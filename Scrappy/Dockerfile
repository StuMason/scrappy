FROM public.ecr.aws/lambda/python:3.11 as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/ && \
    ls -la /opt/ && \
    rm /tmp/chromedriver.zip && \
    rm /tmp/chrome-linux.zip

FROM public.ecr.aws/lambda/python:3.11 as final-stage

RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y

COPY --from=build /opt/chrome-linux64 /opt/chrome
COPY --from=build /opt/chromedriver-linux64/chromedriver /opt/chromedriver

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt -t .

COPY *.py ./

CMD ["handler.handle"]