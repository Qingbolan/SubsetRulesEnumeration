from peewee import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

db = SqliteDatabase('data.db')


class Sample(Model):
    m = IntegerField()
    n = IntegerField()
    k = IntegerField()
    j = IntegerField()
    s = IntegerField()
    gid = IntegerField()
    temp = TextField()
    l = IntegerField()

    class Meta:
        database = db

    def __str__(self):
        return f"Sample {self.id}: m={self.m}, n={self.n}, k={self.k}, j={self.j}, s={self.s}, gid={self.gid}, temp={self.temp}, l={self.l}"

    @staticmethod
    def create_table(**kwargs):
        with db:
            db.create_tables([Sample])

    @staticmethod
    def add_sample(m, n, k, j, s, gid, temp, l):
        sample = Sample(m=m, n=n, k=k, j=j, s=s, gid=gid, temp=temp, l=l)
        sample.save()

    @staticmethod
    def get_sample_by_id(id):
        return Sample.get_or_none(id=id)

    @staticmethod
    def get_samples():
        return Sample.select()

    @staticmethod
    def get_samples_by_gid(gid):
        return Sample.select().where(Sample.gid == gid)

    @staticmethod
    def delete_sample_by_id(id):
        Sample.delete_by_id(id)

    @staticmethod
    def generate_pdf():
        samples = Sample.select()
        c = canvas.Canvas("samples.pdf", pagesize=letter)
        y = 720
        for sample in samples:
            c.drawString(100, y, str(sample))
            y -= 20
            if y <= 50:
                c.showPage()
                y = 720
        c.save()
