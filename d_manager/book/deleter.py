import yaml

from d_manager.book.helper import InteractiveHelper


class DeleterBase:
    def __init__(self):
        pass

    def delete(self, entries):
        raise NotImplementedError


class ProductFoodDeleter:
    def __init__(self, target_id):
        self.__target_id = int(target_id)
        super(ProductFoodDeleter, self).__init__()

    def delete(self, entries):
        found = False
        confirm = False

        for e in entries.values():
            if e.id == self.__target_id:
                found = True
                print('以下を削除しますが、よろしいですか？')
                print(yaml.dump(e.to_dict(), allow_unicode=True))
                confirm = InteractiveHelper.confirm_yes_of_no()
                if not confirm:
                    print('削除がキャンセルされました。')

        else:
            if found and confirm:
                del entries[self.__target_id]
                print('id {} を削除しました。'.format(self.__target_id))
            elif not found:
                raise Exception('id {} は見つかりませんでした。'.format(self.__target_id))
