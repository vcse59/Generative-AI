# Use Node.js with Debian-based dependencies
FROM node:18-bullseye AS builder

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH="${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/emulator:${ANDROID_HOME}/build-tools/33.0.2:$PATH"

# Install required dependencies
RUN apt-get update \
    && apt-get install -y \
    curl \
    git \
    unzip \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install Android SDK and command-line tools
RUN mkdir -p $ANDROID_HOME/cmdline-tools
RUN curl -fo sdk-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-10406996_latest.zip
RUN unzip sdk-tools.zip -d $ANDROID_HOME/cmdline-tools
RUN rm sdk-tools.zip
RUN mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest

# ✅ Set correct sdkmanager path
ENV PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH

# ✅ Ensure correct Java version before running sdkmanager
RUN java -version

# Accept SDK licenses
RUN yes | sdkmanager --licenses

# Install essential Android SDK packages
RUN sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.2" "emulator" "extras;google;m2repository"

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./ 

# Install project dependencies
RUN npm install

# Copy the rest of the project files
COPY . .

# Expose port 8080 for serving the app
EXPOSE 8080

# Serve the app using the `serve` package
CMD ["npm", "run", "web"]
