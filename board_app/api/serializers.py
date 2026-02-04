from rest_framework import serializers
from board_app.models import Board
from task_app.models import Task
from task_app.api.serializers import TaskSerializer
from django.contrib.auth.models import User

class BoardDashboardSerializer(serializers.ModelSerializer):

    member_count=serializers.SerializerMethodField()
    ticket_count=serializers.SerializerMethodField()
    tasks_to_do_count=serializers.SerializerMethodField()
    tasks_high_prio_count=serializers.SerializerMethodField()

    class Meta:
        model=Board
        fields=[
                "id",
                "title",
                "member_count",
                "ticket_count",
                "tasks_to_do_count",
                "tasks_high_prio_count",
                "owner_id"
        ]

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()
    
    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()
    
class BoardCreateSerializer(serializers.ModelSerializer):
        members = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(),
            many=True,
            required=False,
            write_only=True
        )

        class Meta: 
            model = Board
            fields = [
                "id",
                "title",
                "members"
            ]
            read_only_fields = ["id"]

        def create(self, validated_data):
            #entfernt members aus den validen Daten und gibt den Wert zurück
            members = validated_data.pop("members", [])
            #aktueller HTTP-Request
            request_user = self.context["request"].user

            board = Board.objects.create(
                #holt den Titel aus dem Request
                title=validated_data["title"],
                #Owner wird der User, der den Request absetzt
                owner=request_user
            )

            # Owner immer als Member hinzufügen
            board.members.add(request_user, *members)

            return board
        
class BoardMemberSerializer(serializers.ModelSerializer):
        fullname = serializers.CharField(source="userprofile.fullname")

        class Meta:
            model = User
            fields = ["id", "email", "fullname"]

             
class SingleBoardDetailSerializer(serializers.ModelSerializer):
        members = BoardMemberSerializer(many=True, read_only=True)
        tasks = TaskSerializer(many=True, read_only=True)
        owner_id = serializers.IntegerField(source="owner.id", read_only=True)

        class Meta:
            model = Board
            fields = ["id", "title", "owner_id", "members", "tasks"]

class BoardUpdateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Board
        fields = ["title", "members"]

    def update(self, instance, validated_data):
        members = validated_data.pop("members", None)

        # normale Feld-Updates (z. B. title)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # 🔥 MEMBERS ERSETZEN (Soll-Zustand!)
        if members is not None:
            instance.members.set(members)

        return instance



class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    owner_data = BoardMemberSerializer(source="owner", read_only=True)
    members_data = BoardMemberSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data"]


class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField()