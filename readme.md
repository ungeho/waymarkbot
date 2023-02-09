waymark pluginの座標編集用のbot


* /waymark

    /waymark r=[unsigned float] ang=[float]

    半径rと角度angの指定が必須

    その他のパラメーターとして

    マップの中心座標を指定するcx,cy,cz（cyは高さである事に注意）が指定できる。

    cx=[float] (default:100)

    cy=[float] (default:0)

    cz=[float] (default:100)

    また、cirの値を指定する事で、angで指定した角度から時計回りにcir等分した円周上の座標が表示される。

    cir=[int] (default:1)

    これらの値を指定しなかった場合、defaultの値に設定される。

    例えば、フィールドの中心座標が50,100,50で半径10mの円周上に角度90度（北から）8個のマーカーを均等に置きたい場合、以下のように指定する

    /waymark r=10 ang=90 cx=50 cy=100 cz=50 cir=8

* /spread

    /spread r=[unsigned float]

    散開する半径rの指定が必須

    その他のパラメーターとして

    AoEの半径aoe,散開する人数people（2から8まで指定可能）が指定できる。

    aoe = [unsingned float] (default:6)

    people = [int] (default:8)

    指定された人数peopleが半径rの距離で等角度に散開した時にAoEが重なるかを判定する。

    例えば、半径5mのAoEが4人に付与され、半径3mの円周上で散開しても問題ないか確認したい場合、以下のように指定する

    /spread aoe=5 people=4 r=3