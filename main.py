import requests                                        import json                                            import asyncio
import logging                                         from openai import OpenAI                              from os import getenv
from aiogram import Bot, Dispatcher, types             from aiogram.filters.command import Command            from datetime import datetime
from aiogram import F                                  from aiogram.types import Message                      from aiogram.filters import Command
from aiogram.enums import ParseMode                    import pickle
import subprocess
from keys import key

bearer = "Bearer " + key

