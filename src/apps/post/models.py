from django.db import models



class Category(models.Model):
    name=models.CharField("Название",max_length=100)
    image=models.ImageField('Картинка', upload_to='category/image/',  default='category/default.jpg')
    slug = models.SlugField("Слак", max_length=100)
    description=models.TextField("Описание", null=True,blank=True)
    parent = models.ForeignKey(
        "self", 
        on_delete=models.PROTECT, 
        related_name="subcategories",
        null=True,
        blank=True
    )
    
    class Meta: 
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name
    

class Service(models.Model):
    image=models.ImageField('Иконка', upload_to='service/image/', default='service/default.jpg')
    name=models.CharField("Название",max_length=100)
    description=models.TextField("Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField(Category)
    

    class Meta: 
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name
    

class Review(models.Model):
    patient = models.ForeignKey('account.Patient', on_delete=models.CASCADE, null=False)
    doctor = models.ForeignKey('account.Doctor', on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    comment = models.TextField()

    class Meta: 
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.id} Озыв {self.patient} для {self.doctor} {self.comment}"

class AboutType(models.TextChoices):
    ABOUT = "about", "About"
    DOCTORS = "doctors", "Doctors"
    SERVICES = "services", "Services"
    CATEGORIES = "categories", "cateogories"
    INDEX ='index', 'index'
    FAQ='faq', 'faq'
    GALLERY='gallery', 'gallery'


class About(models.Model):

    page = models.CharField(max_length=30, verbose_name="Страница", choices=AboutType.choices, null=True)
    description=models.TextField('Описание')
    image=models.ImageField("Картинка", upload_to="post/image/", blank=True, null=True)


    class Meta:
        verbose_name='Описание'

    def __str__(self):
        return self.description

    
class Contacts(models.Model):
    address=models.CharField(max_length=200, null=True, blank=True)
    email=models.EmailField(max_length=100,null=True, blank=True)
    cell=models.CharField(max_length=100,null=True, blank=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name='Контакты'

    def __str__(self):
        return self.address



class Rewards(models.Model):
    name=models.TextField('Название', null=True)
    description=models.TextField('Описание', null=True)
    image=models.ImageField("Картинка", upload_to="post/image/", blank=True, null=True)

    class Meta:
        verbose_name='Награда'
        verbose_name_plural = "Награды"

    def __str__(self):
        return self.description



class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"


class Gallery(models.Model):
    image=models.ImageField("Картинка", upload_to="post/image/", blank=True, null=True)
    
    class Meta:
        verbose_name='Галерея'
        verbose_name_plural = "Галерея"

class Privacy(models.Model):
    title=models.CharField('Глава', max_length=250, blank=True, null=True)
    description=models.TextField('Описание', null=True)

    class Meta:
        verbose_name = "Конфедициальность"

    def __str__(self):
        return self.description

    