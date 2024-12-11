from core.config import get_connections, conntecions_params, MQ_EXCHANGE, MQ_ROUTING_KEY
from uitils.utils import log
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


def process_new_message(
    ch: "BlockingChannel",
    mehtod: "Basic.Deliver",
    propites: "BasicProperties",
    body: bytes,
):
    log.info("ch %s", ch)
    log.info("method %s", mehtod)
    log.info("properties %s", propites)
    log.info("body %s", body)
    log.warning("Finishhed Process %r", body)


def consume_message(chanel: "BlockingChannel") -> None:
    chanel.basic_consume(
        queue=MQ_ROUTING_KEY, on_message_callback=process_new_message, auto_ack=True
    )

    log.info("Waiting Messages")
    chanel.start_consuming()


def main():
    connection = get_connections()
    with get_connections() as connection:
        log.info("Created Connections: %s", connection)
        with connection.channel() as chanel:
            log.info("Created Chanel: %s", chanel)
            consume_message(chanel=chanel)

    while True:
        pass


if __name__ == "__main__":
    main()
