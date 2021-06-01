from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey

from sqlalchemy.orm import declarative_base, relationship, backref

Base = declarative_base()


class CampaignModel(Base):
    __tablename__ = 'campaign'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    campaign_picture_url = Column(String)
    printer_id = Column(Integer, ForeignKey('printers.id'))
    pledge_price = Column(DECIMAL)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    min_pledgers = Column(Integer)
    max_pledgers = Column(Integer)

    printer = relationship("PrinterModel")
    tech_detail = relationship("TechDetailsModel", uselist=False, back_populates='campaign')
    pledges = relationship('PledgeModel')
    images = relationship('CampaignModelImageModel')

    def __repr__(self):
        return "<Campaign(id='{id}}',name='{name}')>".format(id=self.id, name=self.name)


class PrinterModel(Base):
    __tablename__ = 'printers'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("UserModel", uselist=False, back_populates="printer")

    def __repr__(self):
        return "<Printer(id='{id}}')>".format(id=self.id)


class BuyerModel(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("UserModel", backref=backref("buyers", uselist=False))

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

    printer = relationship("PrinterModel", back_populates="user")

    def __repr__(self):
        return "<User(id='{id}}',username='{user_name}')>".format(id=self.id, user_name=self.user_name)


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


class PledgeModel(Base):
    __tablename__ = 'pledges'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    pledge_price = Column(DECIMAL)
    buyer_id = Column(Integer)
    pledge_date = Column(DateTime)

    def __repr__(self):
        return "<Pledge(id='{id}}',campaign_id='{campaign_id}',buyer_id='{buyer_id}')>"\
            .format(id=self.id, campaign_id=self.campaign_id,buyer_id=self.buyer_id)


class CampaignModelImageModel(Base):
    __tablename__ = 'campaign_model_images'

    id = Column(Integer, primary_key=True)
    model_picture_url = Column(String)
    campaign_id = Column(Integer, ForeignKey('campaign.id'))

    def __repr__(self):
        return "<CampaignModelImage(id='{id}}',campaign_id='{campaign_id}',picture_url='{picture_url}')>"\
            .format(id=self.id, campaign_id=self.campaign_id,picture_url=self.model_picture_url)
