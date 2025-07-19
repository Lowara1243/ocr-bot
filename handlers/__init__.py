from aiogram import Router

def setup_handlers(router: Router):
    from . import user_handlers

    user_handlers.register_user_handlers(router)
