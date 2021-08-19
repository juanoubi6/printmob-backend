import uuid

from my_app.api.domain import Page, Campaign, CampaignModelImage, CampaignModelImagePrototype, File, Order
from my_app.api.domain.campaign import CampaignPrototype, CampaignStatus
from my_app.api.exceptions import CancellationException
from my_app.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException

PRINTER_NOT_FOUND = 'El impresor asociado a la campaña no existe'
CAMPAIGN_CANNOT_BE_CANCELLED = 'La campaña ya no puede ser cancelada'


class CampaignService:
    def __init__(self,
                 campaign_repository,
                 printer_repository,
                 s3_repository):
        self.campaign_repository = campaign_repository
        self.printer_repository = printer_repository
        self.s3_repository = s3_repository

    def create_data(self):
        self.campaign_repository.init_campaigns()

    def create_campaign(self, prototype: CampaignPrototype) -> Campaign:
        self._validate_campaign_printer(prototype)

        return self.campaign_repository.create_campaign(prototype)

    def _validate_campaign_printer(self, prototype):
        if not self.printer_repository.exists_printer(prototype.printer_id):
            raise UnprocessableEntityException(PRINTER_NOT_FOUND)

    def get_campaigns(self, filters: dict) -> Page[Campaign]:
        return self.campaign_repository.get_campaigns(filters)

    def get_campaign_detail(self, campaign_id: int) -> Campaign:
        return self.campaign_repository.get_campaign_detail(campaign_id)

    def create_campaign_model_image(self, campaign_id: int, image: File) -> CampaignModelImage:
        file_name = self._generate_campaign_model_image_name()
        image_url = self.s3_repository.upload_file(image, file_name)

        campaign_model_image_prototype = CampaignModelImagePrototype(
            campaign_id=campaign_id,
            file_name=file_name,
            model_picture_url=image_url
        )

        return self.campaign_repository.create_campaign_model_image(campaign_model_image_prototype)

    def delete_campaign_model_image(self, campaign_model_image_id: int):
        deleted_campaign_model_image = self.campaign_repository.delete_campaign_model_image(campaign_model_image_id)
        self.s3_repository.delete_file(deleted_campaign_model_image.file_name)

    def get_campaign_orders(self, campaign_id: int, filters: dict) -> Page[Order]:
        return self.campaign_repository.get_campaign_orders(campaign_id, filters)

    def get_buyer_campaigns(self, buyer_id: int, filters: dict) -> Page[Campaign]:
        return self.campaign_repository.get_buyer_campaigns(buyer_id, filters)

    def _generate_campaign_model_image_name(self) -> str:
        return "campaign_model_images/{}".format(uuid.uuid4())

    def cancel_campaign(self, campaign_id: int):
        campaign = self.campaign_repository.get_campaign_detail(campaign_id)

        if not campaign.can_be_cancelled():
            raise CancellationException(CAMPAIGN_CANNOT_BE_CANCELLED)

        self.campaign_repository.change_campaign_status(campaign_id, CampaignStatus.TO_BE_CANCELLED)
