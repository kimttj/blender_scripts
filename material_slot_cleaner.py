#　material_slot_cleaner
# マテリアルスロットをソートし、空スロットを削除する。
# 

import bpy

def sort_mslot(obj, ary_mslot, jj):
    """
        機能概要：マテリアルスロットソート処理
                マテリアル名称の文字列比較により昇順に配列を入れ替える。
                空スロットは並び変え優先度低とする。

        引数：
                ary: list  : 並び変えリスト
                jj  : int  : 配列インデックス
        戻り値： なし
    """

    # マテリアルスロットが空だとNoneを返すのでその処理
    ary_none = (ary_mslot[jj].material is None, ary_mslot[jj+1].material is None)
    if ary_none in [(True, True), (False, True)]:
        swap = False
    elif ary_none in [(True, False)]:
        swap = True
    else:
        # マテリアル名に応じて入れ替える
        if ary_mslot[jj].material.name > ary_mslot[jj+1].material.name:
            swap = True
        else:
            swap = False
    
    if swap:
        obj.active_material_index = jj
        bpy.ops.object.material_slot_move(direction='DOWN')

def execute():
    """ メイン処理 """

    obj = bpy.context.object
    ary_mslot = obj.material_slots

    # マテリアルスロットソート
    for ii in range(len(ary_mslot)):
        for jj in range(len(ary_mslot)-2, ii-1, -1):
            sort_mslot(obj, ary_mslot, jj)

    # マテリアルの空スロット削除
    for obj in bpy.data.objects:
        bpy.context.view_layer.objects.active = obj
        if not len(obj.material_slots) == 0:
            for slot in obj.material_slots:
                if slot.name == "":
                    bpy.ops.object.material_slot_remove()


if __name__ == "__main__":
    """ メイン """
    execute()
