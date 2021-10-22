from my_app.api.domain import Order, Campaign, Model
from my_app.api.domain import User
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
    email_body = """La campaña '{name}', en la que participaste con ${price}, finalizo con éxito. Te dejamos los datos del vendedor para que puedas contactarlo ante cualquier duda que tengas.
        
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
    email_body = """La campaña '{name}', en la que participaste con ${price}, lamentablemente no pudo alcanzar su objetivo mínimo. En los próximos días recuperarás el monto de tu reserva en el mismo medio de pago que utilizaste.

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
    email_body = """La campaña '{name}' que creaste finalizo con éxito. En las próximas horas actualizaremos tu saldo disponible para que puedas retirarlo y empezar a imprimir.

    Saludos!
    """.format(name=campaign.name)

    return Email(
        to=receiver,
        subject="Una campaña que creaste finalizo con éxito!",
        body=email_body
    )


def create_unsatisfied_campaign_email_for_printer(receiver: str, campaign: CampaignModel) -> Email:
    email_body = """La campaña '{name}' que creaste lamentablemente ha finalizado sin alcanzar el objetivo que estableciste. A no bajar los brazos!, podes crear otra campaña cuando quieras.

    Saludos!
    """.format(name=campaign.name)

    return Email(
        to=receiver,
        subject="Una campaña que creaste no alcanzo su objetivo",
        body=email_body
    )


def create_updated_order_status_email_for_buyer(receiver: str, campaign: Campaign, order: Order) -> Email:
    email_body = """Tu orden de la campaña '{campaign_name}' fue actualizada. Su estado actual es '{status}'. Para mayor detalle, ingresá en tu dashboard 'Mis Campañas' y revisa tu órden.

    Saludos!
    """.format(campaign_name=campaign.name, status=order.get_translated_order_status())

    return Email(
        to=receiver,
        subject="Una de tus órdenes fue actualizada",
        body=email_body
    )


def create_updated_order_email_for_buyer(receiver: str, campaign: Campaign) -> Email:
    email_body = """Tu orden realizada sobre la campaña '{campaign_name}' fue actualizada. Si querés saber más datos acerca del estado de tus órdenes, ingresá en tu dashboard 'Mis Campañas" y revisa tu órden.

    Saludos!
    """.format(campaign_name=campaign.name)

    return Email(
        to=receiver,
        subject="Una de tus órdenes fue actualizada",
        body=email_body
    )


def create_cancelled_campaign_email_for_client(receiver: str, campaign: CampaignModel) -> Email:
    email_body = """La campaña '{name}', en la que participaste con ${price}, lamentablemente fue cancelada. En los próximos días recuperarás el monto de tu reserva en el mismo medio de pago que utilizaste.

    Saludos!
    """.format(
        name=campaign.name,
        price=campaign.pledge_price,
    )

    return Email(
        to=receiver,
        subject="Una campaña en la que participastes fue cancelada",
        body=email_body
    )


def create_money_request_email(receiver: str, user: User, amount: float) -> Email:
    email_body = """El usuario '{id}' ha solicitado la transferencia de ${amount} a su cuenta.""".format(
        id=user.id,
        amount=amount,
    )

    return Email(
        to=receiver,
        subject="El usuario {} ha solicitado una transferencia".format(user.id),
        body=email_body
    )


def create_model_purchase_email(receiver: str, model: Model) -> Email:
    email_body = """
        Tu modelo '{name}' fue comprador por un usuario. En las próximas horas actualizaremos tu saldo disponible para que puedas retirarlo.

        Saludos!
    """.format(name=model.name,)

    return Email(
        to=receiver,
        subject="Uno de tus modelos fue vendido!",
        body=email_body
    )


def create_completed_campaign_email_with_model_file_url_for_printer(
        receiver: str, campaign: CampaignModel, file_url: str
) -> Email:
    email_body = """
        La campaña '{name}' que creaste finalizo con éxito. En las próximas horas actualizaremos tu saldo disponible para que puedas retirarlo y empezar a imprimir.
        
        Además, te enviamos el link al archivo STL del modelo asociado a la campaña para que puedas comenzar a imprimirlo. Recorda que no podés utilizar este archivo por fuera de la plataforma o estarías incumpliendo los términos y condiciones.
        
        Link al archivo STL: {file_url}

        Saludos!
    """.format(name=campaign.name, file_url=file_url)

    return Email(
        to=receiver,
        subject="Una campaña que creaste finalizo con éxito!",
        body=email_body
    )
