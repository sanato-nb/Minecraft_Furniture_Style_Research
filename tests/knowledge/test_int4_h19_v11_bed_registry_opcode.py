"""H19 synthetic negative controls: no mock run grants real Minecraft approval."""
import unittest

from mcfr import int4_h19_v11_bed_registry_opcode as h19

MAPPING = """net.minecraft.world.level.block.entity.BlockEntityType -> eld:
    public static final net.minecraft.world.level.block.entity.BlockEntityType BED -> b
    public static final net.minecraft.world.level.block.entity.BlockEntityType CHEST -> c
    23:27:void something() -> a
net.minecraft.client.renderer.blockentity.BedRenderer -> hrf:
    void render() -> a
net.minecraft.client.renderer.blockentity.BlockEntityRenderers -> hrk:
    void bootstrap() -> b
"""

BOOTSTRAP="""BootstrapMethods:
  0: #100 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(...)V
    Method arguments:
      #11 ()Ljava/lang/Object;
      #12 REF_newInvokeSpecial hrf."<init>":(Lhrj$a;)V
      #13 ()Lhrf;
  1: #100 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(...)V
    Method arguments:
      #20 REF_newInvokeSpecial other."<init>":()V
InnerClasses:
  public static #11= #12;
"""

REGISTRY="""static {};
    Code:
       0: getstatic     #40       // Field eld.b:Leld;
       3: invokedynamic #55,  0  // InvokeDynamic #0:create:()Lhrj$a;
       8: invokestatic  #60       // Method a:(Leld;Lhrj$a;)V
      11: getstatic     #41       // Field eld.c:Leld;
      14: invokedynamic #56,  0  // InvokeDynamic #1:create:()Lhrj$a;
      19: invokestatic  #60       // Method a:(Leld;Lhrj$a;)V
      22: return
"""+BOOTSTRAP


class H19V11BedRegistration(unittest.TestCase):
    def test_original_field_scope_exact(self):
        self.assertEqual(h19.mapped_field(MAPPING,h19.BLOCK_ENTITY_TYPE,"BED"),"b")

    def test_unmapped_wrong_name_denied(self):
        with self.assertRaisesRegex(ValueError,"MISSING_OR_AMBIGUOUS"):
            h19.mapped_field(MAPPING,h19.BLOCK_ENTITY_TYPE,"FURNACE")

    def test_mappings_can_omit_modifiers_but_field_type_remains_exact(self):
        modified=MAPPING.replace("public static final net.minecraft.world.level.block.entity.BlockEntityType BED",
                                 "net.minecraft.world.level.block.entity.BlockEntityType BED")
        self.assertEqual(h19.mapped_field(modified,h19.BLOCK_ENTITY_TYPE,"BED"),"b")
        wrong=modified.replace("net.minecraft.world.level.block.entity.BlockEntityType BED",
                               "java.lang.String BED")
        with self.assertRaisesRegex(ValueError,"WRONG_TYPE"):
            h19.mapped_field(wrong,h19.BLOCK_ENTITY_TYPE,"BED")

    def test_bytecode_flags_must_prove_public_static_final(self):
        text="""public static final eld b;
           descriptor: Leld;
           flags: (0x0019) ACC_PUBLIC, ACC_STATIC, ACC_FINAL
"""
        self.assertEqual(h19.confirm_bed_field_flags(text,"eld","b"),
                         ["ACC_FINAL","ACC_PUBLIC","ACC_STATIC"])
        with self.assertRaisesRegex(ValueError,"FLAGS_NOT_PUBLIC_STATIC_FINAL"):
            h19.confirm_bed_field_flags(text.replace("ACC_STATIC, ",""),"eld","b")

    def test_duplicate_bed_mapping_denied(self):
        bad=MAPPING.replace("    public static final net.minecraft.world.level.block.entity.BlockEntityType CHEST -> c",
                            "    public static final net.minecraft.world.level.block.entity.BlockEntityType BED -> c")
        with self.assertRaisesRegex(ValueError,"MISSING_OR_AMBIGUOUS"):
            h19.mapped_field(bad,h19.BLOCK_ENTITY_TYPE,"BED")

    def test_javap_inspects_real_opcode_sequence(self):
        r=h19.find_bed_registration(REGISTRY,"eld","b","hrf")
        self.assertEqual((r["block_entity_type_BED_getstatic_pc"],
                          r["bed_renderer_lambda_invokedynamic_pc"],
                          r["registration_invokestatic_pc"],
                          r["bootstrap_index"]),(0,3,8,0))

    def test_bootstrap_wrong_constructor_not_approved(self):
        with self.assertRaisesRegex(ValueError,"NOT_PROVEN"):
            h19.find_bed_registration(REGISTRY.replace(
                'REF_newInvokeSpecial hrf."<init>"',
                'REF_newInvokeSpecial other."<init>"'),"eld","b","hrf")

    def test_bed_field_without_following_register_not_approved(self):
        with self.assertRaisesRegex(ValueError,"NOT_PROVEN"):
            h19.find_bed_registration(REGISTRY.replace(
                "8: invokestatic  #60", "8: invokevirtual #60"),"eld","b","hrf")

    def test_chest_field_cannot_substitute_bed_field(self):
        with self.assertRaisesRegex(ValueError,"NOT_PROVEN"):
            h19.find_bed_registration(REGISTRY.replace(
                "0: getstatic     #40       // Field eld.b:Leld;",
                "0: getstatic     #40       // Field eld.c:Leld;"),"eld","b","hrf")

    def test_wrong_invokedynamic_slot_is_not_the_bed_constructor(self):
        with self.assertRaisesRegex(ValueError,"NOT_PROVEN"):
            h19.find_bed_registration(REGISTRY.replace(
                "InvokeDynamic #0:create","InvokeDynamic #1:create"),"eld","b","hrf")

    def test_registration_requires_exact_entity_type_parameter(self):
        with self.assertRaisesRegex(ValueError,"NOT_PROVEN"):
            h19.find_bed_registration(REGISTRY.replace(
                "Method a:(Leld;Lhrj$a;)V",
                "Method a:(Lstr;Lhrj$a;)V"),"eld","b","hrf")

    def test_duplicate_static_BED_registration_denied(self):
        pair=REGISTRY.split("      11: getstatic")[0]
        copy="""      11: getstatic #40 // Field eld.b:Leld;
      14: invokedynamic #55, 0 // InvokeDynamic #0:create:()Lhrj$a;
      19: invokestatic #60 // Method a:(Leld;Lhrj$a;)V
"""
        bad=pair+copy+BOOTSTRAP
        with self.assertRaisesRegex(ValueError,"DUPLICATED"):
            h19.find_bed_registration(bad,"eld","b","hrf")

    def test_not_dynamically_instrumenting_old_game(self):
        self.assertEqual(h19.h18.VERSION,"1.21.11")
        self.assertEqual(h19.PARENT_STATUS,"PASS_PINNED_OFFICIAL_MOJANG_MAPPING_BED_RENDERER_REGISTRY_STATIC_BYTECODE_LINK")


if __name__=="__main__":
    unittest.main()
