FROM alpine
ENV LANGUAGE="en"
COPY . .
RUN apk add --no-cache ca-certificates &&\
    chmod +x GoBot
EXPOSE 80/tcp
CMD [ "./GoBot" ]