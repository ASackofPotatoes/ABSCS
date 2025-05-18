from django.db import models


class Mnemonic(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default="noName")
    value = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Command(models.Model):
    
    ENCODING_CHOICES = [
        ('ASCII', 'ASCII'),
        ('Binary', 'Binary'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default="noName")
    encoding_type = models.CharField(max_length=10, choices=ENCODING_CHOICES, default='ASCII')
    ascii_content = models.TextField(blank=True, null=True)
    binary_content = models.BinaryField(blank = True, null=True)
    
    @property
    def content(self):
        return self.ascii_content if self.encoding_type == 'ASCII' else self.binary_content

    def set_content(self, value):
        if self.encoding_type == 'ASCII':
            self.ascii_content = value
            self.binary_content = None

        elif self.encoding_type == 'Binary':
            if isinstance(value, str):
                # Remove spaces just in case and validate
                bit_string = value.replace(' ', '')
                if len(bit_string) % 8 != 0 or not set(bit_string).issubset({'0', '1'}):
                    raise ValueError("Binary string must be composed of 0s and 1s in 8-bit chunks.")
                
                # Convert bit string to bytes
                byte_list = [
                    int(bit_string[i:i+8], 2)
                    for i in range(0, len(bit_string), 8)
                ]
                self.binary_content = bytes(byte_list)

            elif isinstance(value, bytes):
                self.binary_content = value

            else:
                raise TypeError("Binary content must be a bytes object or a binary string.")
            
            self.ascii_content = None


class PageMnemonic(models.Model):
    page = models.ForeignKey(
        'Page', on_delete=models.CASCADE, related_name='mnemonics')
    mnemonic = models.ForeignKey(
        'Mnemonic', on_delete=models.SET_NULL, null=True)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('page', 'position')

    def __str__(self):
        return f"{self.page.title} - Mnemonic {self.position}"


class Page(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
