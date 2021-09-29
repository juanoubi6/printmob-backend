import datetime

from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

from my_app.api.domain import Pledge, TechDetail, User, Campaign, CampaignModelImage, Printer, CampaignStatus, Buyer, \
    Address, Order, OrderStatus, UserType, BankInformation, Designer, Model, ModelImage, ModelFile, ModelPurchase, \
    ModelCategory, ModelLike

Base = declarative_base()


class CampaignModel(Base):
    __tablename__ = 'campaign'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    campaign_picture_url = Column(String)
    printer_id = Column(Integer, ForeignKey('printers.id'))
    pledge_price = Column(DECIMAL)
    end_date = Column(DateTime)
    min_pledgers = Column(Integer)
    max_pledgers = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime)
    status = Column(String)
    mp_preference_id = Column(String)

    printer = relationship("PrinterModel")
    tech_detail = relationship("TechDetailsModel", uselist=False, back_populates='campaign')
    pledges = relationship(
        'PledgeModel',
        primaryjoin="and_(CampaignModel.id==PledgeModel.campaign_id, PledgeModel.deleted_at==None)"
    )
    images = relationship('CampaignModelImageModel')

    def __repr__(self):
        return "<Campaign(id='{id}}',name='{name}')>".format(id=self.id, name=self.name)

    def to_campaign_entity(self) -> Campaign:
        return Campaign(
            id=self.id,
            name=self.name,
            description=self.description,
            campaign_picture_url=self.campaign_picture_url,
            campaign_model_images=[ci.to_campaign_model_image_entity() for ci in self.images],
            printer=self.printer.to_printer_entity() if self.printer is not None else None,
            pledge_price=float(self.pledge_price),
            end_date=self.end_date,
            min_pledgers=self.min_pledgers,
            max_pledgers=self.max_pledgers,
            current_pledgers=len(self.pledges),
            tech_details=self.tech_detail.to_tech_detail_entity() if self.tech_detail is not None else None,
            status=CampaignStatus(self.status),
            mp_preference_id=self.mp_preference_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at
        )


class PrinterModel(Base):
    __tablename__ = 'printers'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    bank_information_id = Column(Integer, ForeignKey('bank_information.id'))

    user = relationship("UserModel")
    bank_information = relationship("BankInformationModel")

    def __repr__(self):
        return "<Printer(id='{id}}')>".format(id=self.id)

    def to_printer_entity(self) -> Printer:
        return Printer(
            user=self.user.to_user_entity(),
            bank_information=self.bank_information.to_bank_information_entity()
        )


class BuyerModel(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))

    user = relationship("UserModel")
    address = relationship("AddressModel")

    def to_buyer_entity(self) -> Buyer:
        return Buyer(
            user=self.user.to_user_entity(),
            address=self.address.to_address_entity()
        )

    def __repr__(self):
        return "<Buyer(id='{id}}')>".format(id=self.id)


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    user_name = Column(String)
    date_of_birth = Column(DateTime)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime)
    user_type = Column(String)
    profile_picture_url = Column(String, nullable=True)

    printer = relationship("PrinterModel", uselist=False, back_populates="user")
    buyer = relationship("BuyerModel", uselist=False, back_populates="user")
    designer = relationship("DesignerModel", uselist=False, back_populates="user")

    def __repr__(self):
        return "<User(id='{id}}',username='{user_name}')>".format(id=self.id, user_name=self.user_name)

    def to_user_entity(self) -> User:
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            user_name=self.user_name,
            date_of_birth=self.date_of_birth,
            email=self.email,
            user_type=UserType(self.user_type),
            profile_picture_url=self.profile_picture_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at
        )


class TechDetailsModel(Base):
    __tablename__ = 'tech_details'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    material = Column(String)
    weight = Column(Integer)
    width = Column(Integer)
    length = Column(Integer)
    depth = Column(Integer)

    campaign = relationship('CampaignModel', back_populates='tech_detail')

    def __repr__(self):
        return "<TechDetail(id='{id}}',campaign_id='{campaign_id}')>".format(id=self.id, campaign_id=self.campaign_id)

    def to_tech_detail_entity(self) -> TechDetail:
        return TechDetail(
            id=self.id,
            campaign_id=self.campaign_id,
            material=self.material,
            weight=self.weight,
            width=self.width,
            length=self.length,
            depth=self.depth,
        )


class PledgeModel(Base):
    __tablename__ = 'pledges'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    pledge_price = Column(DECIMAL)
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime)
    printer_transaction_id = Column(Integer, ForeignKey('transactions.id'))

    buyer = relationship("BuyerModel")
    printer_transaction = relationship("TransactionModel")

    def __repr__(self):
        return "<Pledge(id='{id}}',campaign_id='{campaign_id}',buyer_id='{buyer_id}')>" \
            .format(id=self.id, campaign_id=self.campaign_id, buyer_id=self.buyer_id)

    def to_pledge_entity(self) -> Pledge:
        return Pledge(
            id=self.id,
            buyer_id=self.buyer_id,
            pledge_price=float(self.pledge_price),
            campaign_id=self.campaign_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at
        )


class CampaignModelImageModel(Base):
    __tablename__ = 'campaign_model_images'

    id = Column(Integer, primary_key=True)
    model_picture_url = Column(String)
    file_name = Column(String)
    campaign_id = Column(Integer, ForeignKey('campaign.id'))

    def __repr__(self):
        return "<CampaignModelImage(id='{id}}',campaign_id='{campaign_id}',picture_url='{picture_url}')>" \
            .format(id=self.id, campaign_id=self.campaign_id, picture_url=self.model_picture_url)

    def to_campaign_model_image_entity(self) -> CampaignModelImage:
        return CampaignModelImage(
            id=self.id,
            model_picture_url=self.model_picture_url,
            campaign_id=self.campaign_id,
            file_name=self.file_name
        )


class FailedToRefundPledgeModel(Base):
    __tablename__ = 'failed_to_refund_pledges'

    id = Column(Integer, primary_key=True)
    pledge_id = Column(Integer, ForeignKey('pledges.id'))
    fail_date = Column(DateTime)
    error = Column(String)

    def __repr__(self):
        return "<FailedToRefundPledgeModel(id='{id}}',pledge_id='{pledge_id}', error='{error}')>" \
            .format(id=self.id, pledge_id=self.pledge_id, error=self.error)


class AddressModel(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    zip_code = Column(String)
    province = Column(String)
    city = Column(String)
    floor = Column(String)
    apartment = Column(String)

    def __repr__(self):
        return "<Address(id='{id}}',address='{address}',zip_code='{zip_code}')>" \
            .format(id=self.id, address=self.address, zip_code=self.zip_code)

    def to_address_entity(self) -> Address:
        return Address(
            id=self.id,
            address=self.address,
            zip_code=self.zip_code,
            province=self.province,
            city=self.city,
            floor=self.floor,
            apartment=self.apartment
        )


class OrderModel(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    pledge_id = Column(Integer, ForeignKey('pledges.id'))
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    status = Column(String)
    mail_company = Column(String, nullable=True)
    tracking_code = Column(String, nullable=True)
    comments = Column(String, nullable=True)

    buyer = relationship("BuyerModel")
    campaign = relationship("CampaignModel")

    def __repr__(self):
        return "<Order(id='{id}}',campaign_id='{campaign_id}',buyer_id='{buyer_id}')>" \
            .format(id=self.id, campaign_id=self.campaign_id, buyer_id=self.buyer_id)

    def to_order_entity(self) -> Order:
        return Order(
            id=self.id,
            campaign_id=self.campaign_id,
            campaign=self.campaign.to_campaign_entity() if self.campaign is not None else None,
            pledge_id=self.pledge_id,
            buyer=self.buyer.to_buyer_entity(),
            status=OrderStatus(self.status),
            mail_company=self.mail_company,
            tracking_code=self.tracking_code,
            comments=self.comments,
        )


class BankInformationModel(Base):
    __tablename__ = 'bank_information'

    id = Column(Integer, primary_key=True)
    cbu = Column(String)
    alias = Column(String, nullable=True)
    bank = Column(String)
    account_number = Column(String)

    def __repr__(self):
        return "<BankInformation(id='{id}}',cbu='{cbu}',bank='{bank}')>" \
            .format(id=self.id, cbu=self.cbu, bank=self.bank)

    def to_bank_information_entity(self) -> BankInformation:
        return BankInformation(
            id=self.id,
            cbu=self.cbu,
            alias=self.alias,
            bank=self.bank,
            account_number=self.account_number
        )


class TransactionModel(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    mp_payment_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(DECIMAL)
    type = Column(String)
    is_future = Column(Boolean)

    def __repr__(self):
        return "<Transaction(id='{id}}',mp_payment_id='{mp_payment_id}',user_id='{user_id}')>" \
            .format(id=self.id, mp_payment_id=self.mp_payment_id, user_id=self.user_id)


class BalanceRequestModel(Base):
    __tablename__ = 'balance_requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime)

    def __repr__(self):
        return "<BalanceRequest(id='{id}}',user_id='{user_id}',date='{date}')>" \
            .format(id=self.id, user_id=self.user_id, date=self.date)


class DesignerModel(Base):
    __tablename__ = 'designers'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    bank_information_id = Column(Integer, ForeignKey('bank_information.id'))

    user = relationship("UserModel")
    bank_information = relationship("BankInformationModel")

    def __repr__(self):
        return "<Designer(id='{id}}')>".format(id=self.id)

    def to_entity(self) -> Designer:
        return Designer(
            user=self.user.to_user_entity(),
            bank_information=self.bank_information.to_bank_information_entity()
        )


class ModelModel(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    designer_id = Column(Integer, ForeignKey('designers.id'))
    name = Column(String)
    description = Column(String)
    model_file_id = Column(Integer, ForeignKey('model_files.id'))
    model_category_id = Column(Integer, ForeignKey('model_categories.id'))
    likes = Column(Integer)
    width = Column(Integer)
    length = Column(Integer)
    depth = Column(Integer)
    mp_preference_id = Column(String, nullable=True)
    allow_purchases = Column(Boolean)
    allow_alliances = Column(Boolean)
    purchase_price = Column(DECIMAL, nullable=True)
    desired_percentage = Column(DECIMAL, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime)

    designer = relationship("DesignerModel")
    images = relationship('ModelImageModel')
    model_file = relationship('ModelFileModel')
    model_category = relationship('ModelCategoryModel')

    def __repr__(self):
        return "<Model(id='{id}',name='{name}')>".format(id=self.id, name=self.name)

    def to_entity(self, liked_by_user=None) -> Model:
        return Model(
            id=self.id,
            name=self.name,
            description=self.description,
            model_file=self.model_file.to_entity() if self.model_file is not None else None,
            model_category=self.model_category.to_entity() if self.model_category is not None else None,
            width=self.width,
            length=self.length,
            depth=self.depth,
            mp_preference_id=self.mp_preference_id,
            allow_purchases=self.allow_purchases,
            allow_alliances=self.allow_alliances,
            purchase_price=float(self.purchase_price) if self.purchase_price is not None else None,
            desired_percentage=float(self.desired_percentage) if self.desired_percentage is not None else None,
            model_images=[mi.to_entity() for mi in self.images],
            designer=self.designer.to_entity() if self.designer is not None else None,
            likes=self.likes,
            liked_by_user=liked_by_user,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at
        )


class ModelLikeModel(Base):
    __tablename__ = 'model_likes'

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<ModelLike(id='{id}}',model_id='{model_id}', user_id='{user_id}')>".format(
            id=self.id, model_id=self.model_id, user_id=self.user_id
        )

    def to_entity(self) -> ModelLike:
        return ModelLike(
            id=self.id,
            model_id=self.model_id,
            user_id=self.user_id
        )


class ModelImageModel(Base):
    __tablename__ = 'model_images'

    id = Column(Integer, primary_key=True)
    model_picture_url = Column(String)
    file_name = Column(String)
    model_id = Column(Integer, ForeignKey('models.id'))

    def __repr__(self):
        return "<ModelImage(id='{id}}',picture_url='{picture_url}')>".format(id=self.id,
                                                                             picture_url=self.model_picture_url)

    def to_entity(self) -> ModelImage:
        return ModelImage(
            id=self.id,
            model_picture_url=self.model_picture_url,
            model_id=self.model_id,
            file_name=self.file_name
        )


class ModelPurchaseModel(Base):
    __tablename__ = 'model_purchases'

    id = Column(Integer, primary_key=True)
    printer_id = Column(Integer, ForeignKey('printers.id'))
    model_id = Column(Integer, ForeignKey('models.id'))
    price = Column(DECIMAL)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    model = relationship("ModelModel")
    printer = relationship("PrinterModel")

    def __repr__(self):
        return "<ModelPurchase(id='{id}}',price='{price}')>".format(id=self.id, price=self.price)

    def to_entity(self) -> ModelPurchase:
        return ModelPurchase(
            id=self.id,
            printer=self.printer.to_printer_entity() if self.printer is not None else None,
            model=self.model.to_entity() if self.model is not None else None,
            price=float(self.price),
            transaction_id=self.transaction_id,
            created_at=self.created_at,
        )


class ModelFileModel(Base):
    __tablename__ = 'model_files'

    id = Column(Integer, primary_key=True)
    model_file_url = Column(String)
    file_name = Column(String)

    def __repr__(self):
        return "<ModelFile(id='{id}}',model_file_url='{model_file_url}')>".format(id=self.id,
                                                                                  model_file_url=self.model_file_url)

    def to_entity(self) -> ModelFile:
        return ModelFile(
            id=self.id,
            model_file_url=self.model_file_url,
            file_name=self.file_name
        )


class ModelCategoryModel(Base):
    __tablename__ = 'model_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<ModelCategory(id='{id}}',name='{name}')>".format(id=self.id, name=self.name)

    def to_entity(self) -> ModelCategory:
        return ModelCategory(
            id=self.id,
            name=self.name
        )
