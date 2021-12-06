from mongoengine import Document, FloatField, StringField, IntField, DateTimeField, ReferenceField

class Tari(Document):
	nume_tara = StringField(required=True, unique=True)
	latitudine = FloatField(required=True)
	longitudine = FloatField(required=True)


class Orase(Document):
	id_tara = ReferenceField(Tari, required=True, reverse_delete_rule='CASCADE')
	nume_oras = StringField(required=True, unique=True)
	latitudine = FloatField(required=True)
	longitudine = FloatField(required=True)


class Temperaturi(Document):
	id_oras = ReferenceField(Orase, required=True, reverse_delete_rule='CASCADE')
	valoare = FloatField(required=True)
	timestamp = DateTimeField(required=True)
