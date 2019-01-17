FROM slipoh/neo-scan

ENV TZ=Europe/Moscow

RUN set -x \
    && apk add tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

CMD set -x \
    && mix ecto.create \
    && mix ecto.migrate \
    && mix phx.server
