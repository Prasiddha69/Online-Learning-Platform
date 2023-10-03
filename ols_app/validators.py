# from django.core.exceptions import ValidationError
# from django.core.validators import FileValidator

# class FileSizeValidator(FileValidator):
#     def __init__(self, max_size, message=None, code=None):
#         self.max_size = max_size
#         self.message = message or f"File size must be less than {max_size} bytes."
#         self.code = code or 'invalid_file_size'
#         super().__init__(allowed_extensions=['pdf', 'doc', 'docx'], message=self.message, code=self.code)

#     def __call__(self, value):
#         if value.size > self.max_size:
#             raise ValidationError(self.message, code=self.code)
