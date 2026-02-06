from rest_framework import serializers
from django.contrib.auth.models import User

from board_app.models import Board
from task_app.api.serializers import TaskSerializer


class BoardDashboardSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying summarized board information
    on the board dashboard.
    """

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]

    def get_member_count(self, obj):
        """
        Return the number of members assigned to the board.
        """
        return obj.members.count()

    def get_ticket_count(self, obj):
        """
        Return the total number of tasks associated with the board.
        """
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """
        Return the number of tasks with status 'to-do'.
        """
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        """
        Return the number of tasks with high priority.
        """
        return obj.tasks.filter(priority="high").count()


class BoardCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new board.

    Allows assigning members during creation.
    The requesting user is automatically set as the owner
    and added as a board member.
    """

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "members",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """
        Create a new board instance and assign members.

        :param validated_data: Validated input data
        :return: Created Board instance
        """
        members = validated_data.pop("members", [])
        request_user = self.context["request"].user

        board = Board.objects.create(
            title=validated_data["title"],
            owner=request_user,
        )

        board.members.add(request_user, *members)

        return board


class BoardMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for representing board members.
    """

    fullname = serializers.CharField(source="userprofile.fullname")

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class SingleBoardDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed board view including members and tasks.
    """

    members = BoardMemberSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    owner_id = serializers.IntegerField(
        source="owner.id",
        read_only=True,
    )

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
            "members",
            "tasks",
        ]


class BoardUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating board data.

    Supports updating the board title and replacing
    the member list.
    """

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Board
        fields = ["title", "members"]

    def update(self, instance, validated_data):
        """
        Update board attributes and replace members if provided.

        :param instance: Board instance to update
        :param validated_data: Validated input data
        :return: Updated Board instance
        """
        members = validated_data.pop("members", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if members is not None:
            instance.members.set(members)

        return instance


class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for returning board data after an update.
    """

    owner_data = BoardMemberSerializer(
        source="owner",
        read_only=True,
    )
    members_data = BoardMemberSerializer(
        source="members",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_data",
            "members_data",
        ]


class EmailCheckSerializer(serializers.Serializer):
    """
    Serializer for validating an email address.
    """

    email = serializers.EmailField()
