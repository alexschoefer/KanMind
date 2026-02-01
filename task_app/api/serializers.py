from rest_framework import serializers
from task_app.models import Task
from django.contrib.auth.models import User



class TaskUserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="userprofile.fullname")

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class TaskSerializer(serializers.ModelSerializer):
    assignee = TaskUserSerializer(read_only=True)
    reviewer = TaskUserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        if hasattr(obj, "comments"):
            return obj.comments.count()
        return 0

    
class TaskCreateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        write_only=True,
        required=False,
        allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "due_date",
        ]

    def validate(self, data):
        request_user = self.context["request"].user
        board = data["board"]

        def is_member(user):
            return user == board.owner or board.members.filter(id=user.id).exists()

        # Ersteller muss Board-Mitglied sein
        if not is_member(request_user):
            raise serializers.ValidationError(
                "You must be a member of the board to create a task."
            )

        assignee = data.get("assignee")
        reviewer = data.get("reviewer")

        if assignee and not is_member(assignee):
            raise serializers.ValidationError(
                {"assignee_id": "Assignee must be a board member."}
            )

        if reviewer and not is_member(reviewer):
            raise serializers.ValidationError(
                {"reviewer_id": "Reviewer must be a board member."}
            )

        return data


class TaskUpdateSerializer(serializers.ModelSerializer):

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        write_only=True,
        required=False,
        allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model=Task
        fields= [
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "due_date",
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TaskUpdateResponseSerializer(serializers.ModelSerializer):
    assignee = TaskUserSerializer(read_only=True)
    reviewer = TaskUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
        ]
