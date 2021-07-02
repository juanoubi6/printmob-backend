from my_app.api.domain import Order
from my_app.api.repositories.models import CampaignModel


class Email:
    def __init__(
            self,
            to: str,
            subject: str,
            body: str
    ):
        self.to = to
        self.subject = subject
        self.body = body


def create_completed_campaign_email_for_client(receiver: str, campaign: CampaignModel) -> Email:
    email_body = """
        La campaña '{name}', en la que participaste con ${price}, finalizo con éxito. Te dejamos los datos del 
        vendedor para que puedas contactarlo ante cualquier duda que tengas.
        
        Nombre: {first_name} {last_name}
        Email: {email}
    
        Saludos!
    """.format(
        name=campaign.name,
        price=campaign.pledge_price,
        first_name=campaign.printer.user.first_name,
        last_name=campaign.printer.user.last_name,
        email=campaign.printer.user.email
    )

    return Email(
        to=receiver,
        subject="Una campaña en la que participastes finalizo con éxito!",
        body=email_body
    )


def create_unsatisfied_campaign_email_for_client(receiver: str, campaign: CampaignModel) -> Email:
    email_body = """
        La campaña '{name}', en la que participaste con ${price}, lamentablemente no pudo alcanzar su objetivo mínimo. 
        En los próximos días recuperarás el monto de tu reserva en el mismo medio de pago que utilizaste.

        Saludos!
    """.format(
        name=campaign.name,
        price=campaign.pledge_price,
    )

    return Email(
        to=receiver,
        subject="Una campaña en la que participastes no alcanzo su objetivo",
        body=email_body
    )


def create_completed_campaign_email_for_printer(receiver: str, campaign: CampaignModel) -> Email:
    email_body = """
        La campaña '{name}' que creaste finalizo con éxito. En las próximas horas actualizaremos tu saldo disponible
        para que puedas retirarlo y empezar a imprimir.

        Saludos!
    """.format(name=campaign.name)

    return Email(
        to=receiver,
        subject="Una campaña que creaste finalizo con éxito!",
        body=email_body
    )


def create_unsatisfied_campaign_email_for_printer(receiver: str, campaign: CampaignModel) -> Email:
    email_body = """
        La campaña '{name}' que creaste lamentablemente ha finalizado sin alcanzar el objetivo que estableciste. 
        A no bajar los brazos!, podes crear otra campaña cuando quieras.

        Saludos!
    """.format(name=campaign.name)

    return Email(
        to=receiver,
        subject="Una campaña que creaste no alcanzo su objetivo",
        body=email_body
    )


def create_updated_order_status_email_for_buyer(receiver: str, order: Order) -> Email:
    email_body = """
        La orden número #{order_id} que esta a tu nombre fue actualizada. Su estado actual es '{status}'. Si querés 
        saber más datos acerca del estado de tus órdenes, ingresa en la seccion de 'Tus órdenes'.

        Saludos!
    """.format(order_id=order.id, status=order.status.value)

    return Email(
        to=receiver,
        subject="Una de tus órdenes fue actualizada",
        body=email_body
    )
