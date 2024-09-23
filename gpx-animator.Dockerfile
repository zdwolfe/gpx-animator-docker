FROM openjdk:17-jdk-slim
RUN apt-get update && apt-get install -y git
WORKDIR /app
RUN git clone https://github.com/gpx-animator/gpx-animator.git
WORKDIR /app/gpx-animator
RUN ./gradlew build -x test
RUN ln -s $(ls build/libs/*-all.jar) gpx-animator.jar
ENTRYPOINT ["java", "-jar", "gpx-animator.jar"]
