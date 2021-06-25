import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, orm
from sqlalchemy.orm import declarative_base, relationship, backref

from my_app.api.domain import Pledge, TechDetail, User, Campaign, CampaignModelImage, Printer, CampaignStatus

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

    printer = relationship("PrinterModel")
    tech_detail = relationship("TechDetailsModel", uselist=False, back_populates='campaign')
    pledges = relationship(
        'PledgeModel',
        primaryjoin="and_(CampaignModel.id==PledgeModel.campaign_id, PledgeModel.deleted_at==None)"
    )
    images = relationship('CampaignModelImageModel')

    def __repr__(self):
        return "<Campaign(id='{id}}',name='{name}')>".format(id=self.id, name=self.name)

    def to_campaign_entity(self):
        return Campaign(
            id=self.id,
            name=self.name,
            description=self.description,
            campaign_picture_url=self.campaign_picture_url,
            campaign_model_images=[ci.to_campaign_model_image_entity() for ci in self.images],
            printer=Printer(self.printer.user.to_user_entity()) if self.printer is not None else None,
            pledge_price=float(self.pledge_price),
            end_date=self.end_date,
            min_pledgers=self.min_pledgers,
            max_pledgers=self.max_pledgers,
            current_pledgers=len(self.pledges),
            tech_details=self.tech_detail.to_tech_detail_entity() if self.tech_detail is not None else None,
            status=CampaignStatus(self.status),
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at
        )


class PrinterModel(Base):
    __tablename__ = 'printers'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("UserModel", uselist=False, back_populates="printer")

    def __repr__(self):
        return "<Printer(id='{id}}')>".format(id=self.id)

    def to_printer_entity(self):
        return Printer(User(
            id=self.id,
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            user_name=self.user.user_name,
            date_of_birth=self.user.date_of_birth,
            email=self.user.email
        ))


class BuyerModel(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("UserModel", uselist=False, back_populates="buyer")

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

    printer = relationship("PrinterModel", back_populates="user")
    buyer = relationship("BuyerModel", back_populates="user")

    def __repr__(self):
        return "<User(id='{id}}',username='{user_name}')>".format(id=self.id, user_name=self.user_name)

    def to_user_entity(self):
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            user_name=self.user_name,
            date_of_birth=self.date_of_birth,
            email=self.email,
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

    def to_tech_detail_entity(self):
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

    buyer = relationship("BuyerModel")

    def __repr__(self):
        return "<Pledge(id='{id}}',campaign_id='{campaign_id}',buyer_id='{buyer_id}')>" \
            .format(id=self.id, campaign_id=self.campaign_id, buyer_id=self.buyer_id)

    def to_pledge_entity(self):
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

    def to_campaign_model_image_entity(self):
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
