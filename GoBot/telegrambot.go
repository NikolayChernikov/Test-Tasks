package main

import (
	"fmt"
	"github.com/Syfaro/telegram-bot-api"
	"log"
	"os"
	"reflect"
	"time"
)

func telegramBot() {

	bot, err := tgbotapi.NewBotAPI(os.Getenv("TOKEN"))
	if err != nil {
		panic(err)
	}

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates, err := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message == nil {
			continue
		}

		if reflect.TypeOf(update.Message.Text).Kind() == reflect.String && update.Message.Text != "" {

			switch update.Message.Text {
			case "/start":

				msg := tgbotapi.NewMessage(update.Message.Chat.ID, "Hi, i'm a wikipedia bot, i can search information in a wikipedia, send me something what you want find in Wikipedia.")
				_, err = bot.Send(msg)
				if err != nil {
					log.Fatal(err)
				}

			case "/number_of_users":

				if os.Getenv("DB_SWITCH") == "on" {

					num, err := getNumberOfUsers()
					if err != nil {

						msg := tgbotapi.NewMessage(update.Message.Chat.ID, "Database error.")
						_, err = bot.Send(msg)
						if err != nil {
							log.Fatal(err)
						}
					}

					ans := fmt.Sprintf("%d peoples used me for search information in Wikipedia", num)

					msg := tgbotapi.NewMessage(update.Message.Chat.ID, ans)
					_, err = bot.Send(msg)
					if err != nil {
						log.Fatal(err)
					}
				} else {

					msg := tgbotapi.NewMessage(update.Message.Chat.ID, "Database not connected, so i can't say you how many peoples used me.")
					_, err = bot.Send(msg)
					if err != nil {
						log.Fatal(err)
					}
				}
			default:

				language := os.Getenv("LANGUAGE")

				ms, _ := urlEncoded(update.Message.Text)

				url := ms
				request := "https://" + language + ".wikipedia.org/w/api.php?action=opensearch&search=" + url + "&limit=3&origin=*&format=json"

				message := wikipediaAPI(request)

				if os.Getenv("DB_SWITCH") == "on" {

					if err = collectData(update.Message.Chat.UserName, update.Message.Chat.ID, update.Message.Text, message); err != nil {

						msg := tgbotapi.NewMessage(update.Message.Chat.ID, "Database error, but bot still working.")
						_, err = bot.Send(msg)
						if err != nil {
							log.Fatal(err)
						}
					}
				}

				for _, val := range message {

					msg := tgbotapi.NewMessage(update.Message.Chat.ID, val)
					_, err = bot.Send(msg)
					if err != nil {
						log.Fatal(err)
					}
				}
			}
		} else {

			msg := tgbotapi.NewMessage(update.Message.Chat.ID, "Use the words for search.")
			_, err = bot.Send(msg)
			if err != nil {
				log.Fatal(err)
			}
		}
	}
}

func main() {

	time.Sleep(1 * time.Minute)

	if os.Getenv("CREATE_TABLE") == "yes" {

		if os.Getenv("DB_SWITCH") == "on" {

			if err := createTable(); err != nil {

				panic(err)
			}
		}
	}

	time.Sleep(1 * time.Minute)

	//Вызываем бота
	telegramBot()
}
