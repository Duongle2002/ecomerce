from django.db import models
import cloudinary.uploader

class homeimg(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True)

    def save(self, *args, **kwargs):
        # Gọi phương thức save của model cha
        super().save(*args, **kwargs)
        
        # Kiểm tra xem có tệp tin ảnh được tải lên hay không
        if self.image:
            # Tạo đường dẫn cho tệp tin ảnh trên Cloudinary
            cloudinary_path = f"images/{self.image.name}"
            
            # Tải tệp tin ảnh lên Cloudinary
            uploaded_image = cloudinary.uploader.upload(self.image.path, public_id=cloudinary_path)
            
            # Cập nhật đường dẫn tới tệp tin ảnh đã tải lên Cloudinary
            self.image = uploaded_image['secure_url']
            
            # Lưu lại thông tin của model sau khi đã cập nhật
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class upset (models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)
    def save(self, *args, **kwargs):
        # Gọi phương thức save của model cha
        super().save(*args, **kwargs)
        
        # Kiểm tra xem có tệp tin ảnh được tải lên hay không
        if self.image:
            # Tạo đường dẫn cho tệp tin ảnh trên Cloudinary
            cloudinary_path = f"images/{self.image.name}"
            
            # Tải tệp tin ảnh lên Cloudinary
            uploaded_image = cloudinary.uploader.upload(self.image.path, public_id=cloudinary_path)
            
            # Cập nhật đường dẫn tới tệp tin ảnh đã tải lên Cloudinary
            self.image = uploaded_image['secure_url']
            
            # Lưu lại thông tin của model sau khi đã cập nhật
            super().save(*args, **kwargs)
    def __str__(self):
        return self.title    