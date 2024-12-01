FROM openjdk:11-jdk-slim 

WORKDIR /app

CMD ["sh", "-c", "javac Main.java && java Main"]
