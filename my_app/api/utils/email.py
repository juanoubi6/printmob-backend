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
        self.sender = "noreply@printmob.com"


def create_completed_campaign_email(receiver: str, campaign: CampaignModel) -> Email:
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


def create_unsatisfied_campaign_email(receiver: str, campaign: CampaignModel) -> Email:
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
