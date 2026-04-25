from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    # Definimos los campos que esperamos del front (React)
    email = serializers.EmailField(label="Correo electrónico")
    password = serializers.CharField(
        label="Contraseña",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # 1. Buscamos al usuario de forma segura
            # Usamos .filter().first() para evitar errores si el email no es único
            user = User.objects.filter(email=email).first()

            if not user:
                # El error 400 que ves en los logs viene de aquí
                raise serializers.ValidationError('Credenciales inválidas')

            # 2. Autenticamos usando el username real del usuario encontrado
            user = authenticate(username=user.username, password=password)

            if not user:
                raise serializers.ValidationError('Credenciales inválidas')
            
            if not user.is_active:
                raise serializers.ValidationError('Esta cuenta de usuario está inactiva.')
        else:
            raise serializers.ValidationError('Debe incluir "email" y "password".')

        # Guardamos el objeto user para que la View lo pueda usar
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']