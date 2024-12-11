from core.config import get_connections, conntecions_params, MQ_EXCHANGE, MQ_ROUTING_KEY
from uitils.utils import log
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel


def produce_message(chanel: "BlockingChannel") -> None:

    queue = chanel.queue_declare(queue=MQ_ROUTING_KEY)
    log.info("Declared queue %s with details %s", MQ_ROUTING_KEY, queue)

    send_message = "Hello World"
    chanel.basic_publish(
        exchange="",
        routing_key=MQ_ROUTING_KEY,
        body=send_message,
    )
    log.warning("Published Message: %s", send_message)

    while True:
        pass


def main():
    connection = get_connections()
    with get_connections() as connection:
        log.info("Created Connections: %s", connection)
        with connection.channel() as chanel:
            log.info("Created Chanel: %s", chanel)
            produce_message(chanel=chanel)

    while True:
        pass


if __name__ == "__main__":
    main()
