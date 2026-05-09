from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password confirmation.
    
    Validates email uniqueness, password confirmation, and creates a new user.
    """
    username = serializers.CharField(required=False, allow_blank=True)
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        """Validate that passwords match.
        
        Args:
            data (dict): Serializer data containing password and confirmed_password.
            
        Returns:
            dict: Validated data if passwords match.
            
        Raises:
            ValidationError: If passwords do not match.
        """
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError(
                "Bitte überprüfe deine Eingaben und versuche es erneut."
            )
        return data

    def validate_email(self, value):
        """Validate that email is unique in the system.
        
        Args:
            value (str): Email address to validate.
            
        Returns:
            str: Email if valid.
            
        Raises:
            ValidationError: If email already exists in database.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Für diese E-Mail-Adresse existiert bereits ein Konto."
            )
        return value

    def create(self, validated_data):
        """Create a new inactive user and generate activation token.
        
        Args:
            validated_data (dict): Validated user data (email, password).
            
        Returns:
            tuple: (User instance with is_active=False, activation token).
            
        Note:
            User is created with is_active=False and must activate via email link.
        """
        validated_data.pop('confirmed_password')

        user = User(
            username=validated_data.get('username') or validated_data['email'],
            email=validated_data['email'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()

        token = default_token_generator.make_token(user)

        return user, token
    

class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset request.
    
    Validates and accepts email address to initiate password reset process.
    """
    email = serializers.EmailField()



class PasswordConfirmSerializer(serializers.Serializer):
    """Serializer for password confirmation during password reset.
    
    Validates that new password and confirmation password match.
    """
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate that new passwords match.
        
        Args:
            data (dict): Data containing new_password and confirm_password.
            
        Returns:
            dict: Validated data if passwords match.
            
        Raises:
            ValidationError: If passwords do not match.
        """
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                "Bitte überprüfe deine Eingaben und versuche es erneut."
            )
        return data