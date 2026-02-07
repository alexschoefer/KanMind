from rest_framework import serializers
from django.contrib.auth.models import User

from task_app.models import Task, TaskCommentModel


class TaskUserSerializer(serializers.ModelSerializer):
    """
    Serializer for representing a user in task-related contexts.
    """

    fullname = serializers.CharField(source="userprofile.fullname")

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying task details.
    """

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
        """
        Return the number of comments associated with the task.
        """
        if hasattr(obj, "comments"):
            return obj.comments.count()
        return 0


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new task. Handles assignment of assignee and reviewer
    and validates board membership.
    """

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        write_only=True,
        required=False,
        allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False,
        allow_null=True,
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
        """
        Validate task creation rules.

        Ensures that:
        - The creator is a member of the board
        - Assignee and reviewer are board members
        """
        request_user = self.context["request"].user
        board = data["board"]

        def is_member(user):
            return (
                user == board.owner
                or board.members.filter(id=user.id).exists()
            )

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

    def create(self, validated_data):
        """
        Create a new task and assign the requesting user as creator.
        """
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing task.
    """

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        write_only=True,
        required=False,
        allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "due_date",
        ]

    def update(self, instance, validated_data):
        """
        Update task fields with provided values.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TaskUpdateResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for returning task data after an update.
    """

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


# class TaskCommentCreateSerializer(serializers.ModelSerializer):
#     """
#     Serializer for creating a task comment.
#     """

#     author = serializers.SerializerMethodField()

#     class Meta:
#         model = TaskCommentModel
#         fields = [
#             "id",
#             "created_at",
#             "author",
#             "content",
#         ]
#         read_only_fields = ["id", "created_at"]

#     def get_author(self, obj):
#         """
#         Return the full name of the comment author.
#         """
#         return obj.author.userprofile.fullname


class TaskCommentsSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying task comments.
    """

    author = serializers.SerializerMethodField()

    class Meta:
        model = TaskCommentModel
        fields = ["id", "created_at", "author", "content"]

    def get_author(self, obj):
        """
        Return the full name of the comment author.
        """
        return obj.author.userprofile.fullname
