"""Generate a vanilla-command datapack for small C/D runtime tests."""
import argparse
import csv
import json
from itertools import product
from pathlib import Path

A='another_furniture:'
H='handcrafted:'
M='mcwfurnitures:'
SIDES=('single','left','right','middle')


def put(x,y,z,block,props=''):
    return f'setblock {x} {y} {z} {block}'+(f'[{props}]' if props else '')


def states(label,x,y,z,block,choices):
    keys=list(choices)
    result=[]
    for values in product(*choices.values()):
        props=','.join(f'{k}={v}' for k,v in zip(keys,values))
        suffix=','.join(values)
        result.append(f'execute if block {x} {y} {z} {block}[{props}] run say CD_STATE_{label}={suffix}')
    return result


def platforms(z):
    return [
        'time set noon','weather clear','difficulty peaceful',
        f'fill -16 119 {z-2} 12 119 {z+2} minecraft:smooth_stone',
        f'fill -12 120 {z+3} 12 123 {z+3} minecraft:light_gray_concrete',
        put(-11,120,z,'minecraft:stone'),
    ]


def place_early():
    setup=platforms(40)+platforms(56)
    for x, name, props in ((-8,'oak_table','facing=north'),(-7,'oak_table','facing=north'),
                           (-4,'oak_bench','facing=north,back=true'),(-3,'oak_bench','facing=north,back=true'),
                           (0,'oak_shelf','facing=north'),(1,'oak_shelf','facing=north'),
                           (4,'birch_chair','facing=south,tucked=false,variant=1'),
                           (8,'spruce_chair','facing=south,tucked=false,variant=1')):
        setup.append(put(x,120,40,A+name,props))
    for x,name,props in ((-8,'oak_couch','facing=north'),(-7,'oak_couch','facing=north'),
                         (-4,'oak_chair','facing=south'),(0,'oak_bench','facing=south')):
        setup.append(put(x,120,56,H+name,props))

    cases=[
        ('af_table_east',-8,120,40,A+'oak_table',{f'leg_{i}':('false','true') for i in range(1,5)}),
        ('af_table_west',-7,120,40,A+'oak_table',{f'leg_{i}':('false','true') for i in range(1,5)}),
        ('af_bench_left',-4,120,40,A+'oak_bench',{'horizontal_1':SIDES,'horizontal_2':SIDES}),
        ('af_bench_right',-3,120,40,A+'oak_bench',{'horizontal_1':SIDES,'horizontal_2':SIDES}),
        ('af_shelf_left',0,120,40,A+'oak_shelf',{'horizontal':SIDES}),
        ('af_shelf_right',1,120,40,A+'oak_shelf',{'horizontal':SIDES}),
        ('af_birch',4,120,40,A+'birch_chair',{'variant':('1','2','3')}),
        ('af_spruce',8,120,40,A+'spruce_chair',{'variant':('1','2','3')}),
    ]
    shapes=SIDES+('inner_left','inner_right','outer_left','outer_right')
    cases += [('hc_couch_left',-8,120,56,H+'oak_couch',{'shape':shapes}),
              ('hc_couch_right',-7,120,56,H+'oak_couch',{'shape':shapes})]
    for label,x,z in (('hc_bed_click',4,56),('hc_bed_north',4,55),('hc_bed_south',4,57),
                      ('hc_bed_east',5,56),('hc_bed_west',3,56)):
        cases.append((label,x,120,z,H+'oak_fancy_bed',{'part':('foot','head'),'facing':('north','south','east','west')}))
    probes=[('af_air',-14,40),('af_stone',-11,40),('af_table',-8,40),('af_bench',-4,40),
            ('af_chair',4,40),('hc_air',-14,56),('hc_stone',-11,56),('hc_couch',-8,56),
            ('hc_chair',-4,56),('hc_bench',0,56),('hc_bed',4,56)]
    switch={f'variant_{variant}':[put(x,120,40,A+name,f'facing=south,tucked=false,variant={variant}')
              for x,name in ((4,'birch_chair'),(8,'spruce_chair'))] for variant in (1,2,3)}
    return setup, cases, probes, switch


def place_late():
    z=220
    setup=platforms(z)
    for x,y,name,props in ((-8,120,'oak_table',''),(-7,120,'oak_table',''),
                           (-4,120,'oak_desk','facing=north'),(-3,120,'oak_desk','facing=north'),
                           (0,120,'oak_wardrobe','facing=north,hinge=left'),
                           (0,121,'oak_wardrobe','facing=north,hinge=left'),
                           (4,120,'oak_chair','facing=south'),
                           (8,120,'oak_drawer','facing=north'),(9,120,'oak_drawer','facing=north')):
        setup.append(put(x,y,z,M+name,props))
    cases=[]
    table={d:('false','true') for d in ('north','east','west','south')}
    for label,x in (('table_left',-8),('table_right',-7)):
        cases.append(('macaw_'+label,x,120,z,M+'oak_table',table))
    for name,left,right in (('desk',-4,-3),('drawer',8,9)):
        for label,x in (('left',left),('right',right)):
            cases.append((f'macaw_{name}_{label}',x,120,z,M+'oak_'+name,{'connection':SIDES}))
    for label,y in (('lower',120),('upper',121)):
        cases.append(('macaw_wardrobe_'+label,0,y,z,M+'oak_wardrobe',
                      {'connection':('base','middle','bottom','top'),'hinge':('left','right')}))
    probes=[('macaw_air',-14,z),('macaw_stone',-11,z),('macaw_table',-8,z),('macaw_desk',-4,z),
            ('macaw_wardrobe',0,z),('macaw_chair',4,z),('macaw_drawer',8,z)]
    return setup,cases,probes,{}


def wide_matrix():
    setup=platforms(264)
    check=[]
    for index,(kind,facing,axis) in enumerate(product(('desk','drawer'),('north','east'),('x','z'))):
        x=-9+index%4*6
        z=262+index//4*4
        name=M+'oak_'+kind
        for label,dx,dz in (('a',0,0),('b',int(axis=='x'),int(axis=='z'))):
            setup.append(put(x+dx,120,z+dz,name,'facing='+facing))
            ident=f'macaw_matrix_{kind}_{facing}_{axis}_{label}'
            check.extend(states(ident,x+dx,120,z+dz,name,{'facing':(facing,),'connection':SIDES}))
    setup.extend(check)
    return setup


def generated_items(old, ledger):
    with ledger.open(encoding='utf-8', newline='') as stream:
        ids=[row['model'].replace(':item/',':') for row in csv.DictReader(stream)
             if row['status']=='GENERATED_ITEM_RUNTIME' and (row['mod']!='MACAW')==old]
    setup=[]
    checks=[]
    for index, item in enumerate(ids):
        if old:
            z=75+12*(index//28)
            col=index%28%7
            row=index%28//7
            x=6-col*1.7
            y=125-row*1.1
        else:
            z=240
            x=(-1 if index==0 else 2)
            y=123.35
        if index==0 or (old and index==28):
            setup.append(f'fill -8 120 {z+2} 8 127 {z+2} minecraft:light_gray_concrete')
        tag=f'cd_item_{index}'
        nbt={'Tags':['cd_generated',tag], 'billboard':'center','item':{'id':item,'count':1}}
        setup.append(f'summon minecraft:item_display {x} {y} {z} '+json.dumps(nbt,separators=(',',':')))
        filter_nbt=json.dumps({'item':{'id':item}},separators=(',',':'))
        checks.append(f'execute if data entity @e[tag={tag},limit=1] {filter_nbt} run say CD_ITEM_{item}')
    return [*setup,*checks,'say CD_ITEMS_READ']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version',choices=('1.21.1','1.21.11'),required=True)
    parser.add_argument('--pack',type=Path,required=True)
    parser.add_argument('--c-ledger',type=Path,default=Path(__file__).with_name('C_EXCEPTION_RECHECK.csv'))
    args=parser.parse_args()
    old=args.version=='1.21.1'
    setup,cases,probes,extra=(place_early if old else place_late)()
    if not old:
        extra['wide_matrix']=wide_matrix()
    pack=args.pack
    functions=pack/'data/cd_audit/function'
    functions.mkdir(parents=True,exist_ok=True)
    version={'pack_format':48} if old else {'min_format':[94,1],'max_format':[94,1]}
    (pack/'pack.mcmeta').write_text(json.dumps({'pack':{'description':'C/D furniture test fixture',**version}})+'\n')
    check=[cmd for case in cases for cmd in states(*case)]
    spawn=[]
    read=[]
    for name,x,z in probes:
        tag='cd_'+name
        spawn.append(f'summon minecraft:armor_stand {x+0.5} 125 {z+0.5} '
                     +json.dumps({'Tags':['cd_probe',tag]},separators=(',',':')))
        read.append(f'execute store result score {name} cd_probe run data get entity @e[tag={tag},limit=1] Pos[1] 1000')
        message=json.dumps([{'text':f'CD_HEIGHT_{name}='},{'score':{'name':name,'objective':'cd_probe'}}],separators=(',',':'))
        read.append(f'tellraw @a {message}')
    for file,commands in {'place':[*setup,'say CD_PLACED'], 'verify':[*check,'say CD_STATES_READ'],
                          'drop':['kill @e[tag=cd_probe]','scoreboard objectives add cd_probe dummy',*spawn],
                          'height':read,'clear_probe':['kill @e[tag=cd_probe]'],
                          'items':['kill @e[tag=cd_generated]',*generated_items(old,args.c_ledger)], **extra}.items():
        (functions/(file+'.mcfunction')).write_text('\n'.join(commands)+'\n')


if __name__=='__main__':
    main()
