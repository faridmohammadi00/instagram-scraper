"""
Author: Farid Mohammadi
Date: 2024-08-15 09:59:10
LastEditors:
LastEditTime: 2024-08-15 09:59:10
FilePath: insta/serializers.py
"""
from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    pff_number = serializers.DictField()
    profile_picture = serializers.ListField()
    exist_story = serializers.BooleanField()
    h_cover_urls = serializers.ListField()
    h_infos = serializers.DictField()
    bio = serializers.CharField(max_length=500)
    bio_link = serializers.CharField(max_length=240)
    name = serializers.CharField(max_length=50)
