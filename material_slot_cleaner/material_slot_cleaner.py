#　material_slot_cleaner
# 機能概要；
# 選択中のオブジェクトのマテリアルスロットのマテリアル順序を
# 名称順にソートし、空スロットを削除する。
# 

import bpy

def sort_mat_slot(obj, ary_mat_slot, jj):
    """
        機能概要：マテリアルスロットソート処理
                マテリアル名称の文字列比較により昇順に配列を入れ替える。
                空スロットは並び変え優先度低とする。

        引数：
                obj: 処理対象オブジェクト
                ary_mslot: 並び変えマテリアルスロットリスト
                jj  : 配列インデックス
        戻り値： なし
    """

    # マテリアルスロットが空だとNoneを返すのでその処理
    ary_none = (ary_mat_slot[jj].material is None, ary_mat_slot[jj+1].material is None)
    if ary_none in [(True, True), (False, True)]:
        swap = False
    elif ary_none in [(True, False)]:
        swap = True
    else:
        # マテリアル名に応じて入れ替える
        if ary_mat_slot[jj].material.name > ary_mat_slot[jj+1].material.name:
            swap = True
        else:
            swap = False
    
    if swap:
        obj.active_material_index = jj
        bpy.ops.object.material_slot_move(direction='DOWN')

def execute():
    """ メイン処理 """

    # 選択中の複数オブジェクトを処理対象とする
    obj_list = bpy.context.selected_objects

    # マテリアルスロットソート処理
    for obj in obj_list:
        print("処理開始：{}", obj.name)
        bpy.context.view_layer.objects.active = obj        
        ary_mat_slot = obj.material_slots

        # マテリアルスロットソート
        for ii in range(len(ary_mat_slot)):
            for jj in range(len(ary_mat_slot)-2, ii-1, -1):
                sort_mat_slot(obj, ary_mat_slot, jj)

    # マテリアルの空スロット削除
    for obj in obj_list:
        bpy.context.view_layer.objects.active = obj
        if not len(obj.material_slots) == 0:
            for slot in obj.material_slots:
                if slot.name == "":
                    bpy.ops.object.material_slot_remove()


if __name__ == "__main__":
    """ メイン """
    execute()