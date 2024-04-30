class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    session = factory.LazyFunction(lambda: fake.word().upper()[:3] + str(time.time())[-4:])
    name = factory.LazyFunction(lambda: fake.name())
    adress = factory.LazyFunction(lambda: fake.address())
    date_joined = factory.LazyFunction(datetime.now)
    email = factory.LazyAttribute(lambda obj: f'{obj.name.replace(" ", "_").lower()}_{str(time.time())[-3:]}@gmail.com')
    is_superuser = factory.LazyFunction(lambda: random.choice([True, False]))
    is_staff = factory.LazyFunction(lambda: random.choice([True, False]))
    post = factory.LazyFunction(lambda: random.choice(PostService.findAll()))
    role = factory.LazyFunction(lambda: random.choice(RoleService.findAll()))
    
    
    @factory.post_generation        
    def agency(self, create, extracted, **kwargs):
        if not create:
            # La méthode de construction a été appelée explicitement, nous ne faisons rien ici
            return
        if extracted:
            for a in extracted:
                self.agency.add(a)
        else:
            # Sinon, utilisez tous les groupes existants
            agency_random= random.choice(Agency.objects.all())
            print(agency_random)
            self.agency.add(agency_random)



# class ClientFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Client
