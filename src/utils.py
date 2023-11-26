def check_admin(user_id: int):
    with open('admins.txt', 'r') as f:
        admins = f.read().strip().split('\n')
        for admin in admins:
            if int(admin) == user_id:
                return True
    return False


def verification(function_to_decorate):
    async def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        mess = args[0]  # message aiogram type
        print(mess.from_user.id)
        verification_status = check_admin(mess.from_user.id)
        if verification_status:
            return await function_to_decorate(mess, kwargs["state"])
        else:
            await mess.answer(text="Вас нет в списке админов.")
    return a_wrapper_accepting_arbitrary_arguments
