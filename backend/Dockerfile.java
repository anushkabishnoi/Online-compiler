FROM openjdk:latest

WORKDIR /app

COPY . /app

CMD ["sh", "-c", "javac Main.java && java Main"]
