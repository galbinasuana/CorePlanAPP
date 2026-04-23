; ModuleID = 'marshal_methods.x86.ll'
source_filename = "marshal_methods.x86.ll"
target datalayout = "e-m:e-p:32:32-p270:32:32-p271:32:32-p272:64:64-f64:32:64-f80:32-n8:16:32-S128"
target triple = "i686-unknown-linux-android21"

%struct.MarshalMethodName = type {
	i64, ; uint64_t id
	ptr ; char* name
}

%struct.MarshalMethodsManagedClass = type {
	i32, ; uint32_t token
	ptr ; MonoClass klass
}

@assembly_image_cache = dso_local local_unnamed_addr global [327 x ptr] zeroinitializer, align 4

; Each entry maps hash of an assembly name to an index into the `assembly_image_cache` array
@assembly_image_cache_hashes = dso_local local_unnamed_addr constant [648 x i32] [
	i32 2616222, ; 0: System.Net.NetworkInformation.dll => 0x27eb9e => 68
	i32 10166715, ; 1: System.Net.NameResolution.dll => 0x9b21bb => 67
	i32 10266594, ; 2: LiveChartsCore.SkiaSharpView.dll => 0x9ca7e2 => 177
	i32 15721112, ; 3: System.Runtime.Intrinsics.dll => 0xefe298 => 108
	i32 32687329, ; 4: Xamarin.AndroidX.Lifecycle.Runtime => 0x1f2c4e1 => 244
	i32 34715100, ; 5: Xamarin.Google.Guava.ListenableFuture.dll => 0x211b5dc => 278
	i32 34839235, ; 6: System.IO.FileSystem.DriveInfo => 0x2139ac3 => 48
	i32 38948123, ; 7: ar\Microsoft.Maui.Controls.resources.dll => 0x2524d1b => 286
	i32 39485524, ; 8: System.Net.WebSockets.dll => 0x25a8054 => 80
	i32 42244203, ; 9: he\Microsoft.Maui.Controls.resources.dll => 0x284986b => 295
	i32 42639949, ; 10: System.Threading.Thread => 0x28aa24d => 145
	i32 66541672, ; 11: System.Diagnostics.StackTrace => 0x3f75868 => 30
	i32 67008169, ; 12: zh-Hant\Microsoft.Maui.Controls.resources => 0x3fe76a9 => 319
	i32 68219467, ; 13: System.Security.Cryptography.Primitives => 0x410f24b => 124
	i32 72070932, ; 14: Microsoft.Maui.Graphics.dll => 0x44bb714 => 193
	i32 82292897, ; 15: System.Runtime.CompilerServices.VisualC.dll => 0x4e7b0a1 => 102
	i32 83839681, ; 16: ms\Microsoft.Maui.Controls.resources.dll => 0x4ff4ac1 => 303
	i32 101534019, ; 17: Xamarin.AndroidX.SlidingPaneLayout => 0x60d4943 => 262
	i32 117431740, ; 18: System.Runtime.InteropServices => 0x6ffddbc => 107
	i32 120558881, ; 19: Xamarin.AndroidX.SlidingPaneLayout.dll => 0x72f9521 => 262
	i32 122350210, ; 20: System.Threading.Channels.dll => 0x74aea82 => 139
	i32 134690465, ; 21: Xamarin.Kotlin.StdLib.Jdk7.dll => 0x80736a1 => 282
	i32 136584136, ; 22: zh-Hans\Microsoft.Maui.Controls.resources.dll => 0x8241bc8 => 318
	i32 140062828, ; 23: sk\Microsoft.Maui.Controls.resources.dll => 0x859306c => 311
	i32 142721839, ; 24: System.Net.WebHeaderCollection => 0x881c32f => 77
	i32 149972175, ; 25: System.Security.Cryptography.Primitives.dll => 0x8f064cf => 124
	i32 159306688, ; 26: System.ComponentModel.Annotations => 0x97ed3c0 => 13
	i32 165246403, ; 27: Xamarin.AndroidX.Collection.dll => 0x9d975c3 => 218
	i32 172961045, ; 28: Syncfusion.Maui.Core.dll => 0xa4f2d15 => 202
	i32 176265551, ; 29: System.ServiceProcess => 0xa81994f => 132
	i32 182336117, ; 30: Xamarin.AndroidX.SwipeRefreshLayout.dll => 0xade3a75 => 264
	i32 184328833, ; 31: System.ValueTuple.dll => 0xafca281 => 151
	i32 205061960, ; 32: System.ComponentModel => 0xc38ff48 => 18
	i32 209399409, ; 33: Xamarin.AndroidX.Browser.dll => 0xc7b2e71 => 216
	i32 220171995, ; 34: System.Diagnostics.Debug => 0xd1f8edb => 26
	i32 230216969, ; 35: Xamarin.AndroidX.Legacy.Support.Core.Utils.dll => 0xdb8d509 => 238
	i32 230752869, ; 36: Microsoft.CSharp.dll => 0xdc10265 => 1
	i32 231409092, ; 37: System.Linq.Parallel => 0xdcb05c4 => 59
	i32 231814094, ; 38: System.Globalization => 0xdd133ce => 42
	i32 246610117, ; 39: System.Reflection.Emit.Lightweight => 0xeb2f8c5 => 91
	i32 259487786, ; 40: Syncfusion.Maui.Charts => 0xf77782a => 201
	i32 261689757, ; 41: Xamarin.AndroidX.ConstraintLayout.dll => 0xf99119d => 221
	i32 276479776, ; 42: System.Threading.Timer.dll => 0x107abf20 => 147
	i32 278686392, ; 43: Xamarin.AndroidX.Lifecycle.LiveData.dll => 0x109c6ab8 => 240
	i32 280482487, ; 44: Xamarin.AndroidX.Interpolator => 0x10b7d2b7 => 237
	i32 291076382, ; 45: System.IO.Pipes.AccessControl.dll => 0x1159791e => 54
	i32 298918909, ; 46: System.Net.Ping.dll => 0x11d123fd => 69
	i32 317674968, ; 47: vi\Microsoft.Maui.Controls.resources => 0x12ef55d8 => 316
	i32 318968648, ; 48: Xamarin.AndroidX.Activity.dll => 0x13031348 => 207
	i32 321597661, ; 49: System.Numerics => 0x132b30dd => 83
	i32 321963286, ; 50: fr\Microsoft.Maui.Controls.resources.dll => 0x1330c516 => 294
	i32 342366114, ; 51: Xamarin.AndroidX.Lifecycle.Common => 0x146817a2 => 239
	i32 360082299, ; 52: System.ServiceModel.Web => 0x15766b7b => 131
	i32 367780167, ; 53: System.IO.Pipes => 0x15ebe147 => 55
	i32 374914964, ; 54: System.Transactions.Local => 0x1658bf94 => 149
	i32 375677976, ; 55: System.Net.ServicePoint.dll => 0x16646418 => 74
	i32 379916513, ; 56: System.Threading.Thread.dll => 0x16a510e1 => 145
	i32 385762202, ; 57: System.Memory.dll => 0x16fe439a => 62
	i32 392610295, ; 58: System.Threading.ThreadPool.dll => 0x1766c1f7 => 146
	i32 395744057, ; 59: _Microsoft.Android.Resource.Designer => 0x17969339 => 323
	i32 403441872, ; 60: WindowsBase => 0x180c08d0 => 165
	i32 409257351, ; 61: tr\Microsoft.Maui.Controls.resources.dll => 0x1864c587 => 314
	i32 441335492, ; 62: Xamarin.AndroidX.ConstraintLayout.Core => 0x1a4e3ec4 => 222
	i32 442565967, ; 63: System.Collections => 0x1a61054f => 12
	i32 450948140, ; 64: Xamarin.AndroidX.Fragment.dll => 0x1ae0ec2c => 235
	i32 451504562, ; 65: System.Security.Cryptography.X509Certificates => 0x1ae969b2 => 125
	i32 456227837, ; 66: System.Web.HttpUtility.dll => 0x1b317bfd => 152
	i32 459347974, ; 67: System.Runtime.Serialization.Primitives.dll => 0x1b611806 => 113
	i32 465846621, ; 68: mscorlib => 0x1bc4415d => 166
	i32 469710990, ; 69: System.dll => 0x1bff388e => 164
	i32 476646585, ; 70: Xamarin.AndroidX.Interpolator.dll => 0x1c690cb9 => 237
	i32 486930444, ; 71: Xamarin.AndroidX.LocalBroadcastManager.dll => 0x1d05f80c => 250
	i32 489220957, ; 72: es\Microsoft.Maui.Controls.resources.dll => 0x1d28eb5d => 292
	i32 498788369, ; 73: System.ObjectModel => 0x1dbae811 => 84
	i32 513247710, ; 74: Microsoft.Extensions.Primitives.dll => 0x1e9789de => 187
	i32 525008092, ; 75: SkiaSharp.dll => 0x1f4afcdc => 195
	i32 526420162, ; 76: System.Transactions.dll => 0x1f6088c2 => 150
	i32 527452488, ; 77: Xamarin.Kotlin.StdLib.Jdk7 => 0x1f704948 => 282
	i32 530272170, ; 78: System.Linq.Queryable => 0x1f9b4faa => 60
	i32 538707440, ; 79: th\Microsoft.Maui.Controls.resources.dll => 0x201c05f0 => 313
	i32 539058512, ; 80: Microsoft.Extensions.Logging => 0x20216150 => 183
	i32 540030774, ; 81: System.IO.FileSystem.dll => 0x20303736 => 51
	i32 545304856, ; 82: System.Runtime.Extensions => 0x2080b118 => 103
	i32 546455878, ; 83: System.Runtime.Serialization.Xml => 0x20924146 => 114
	i32 549171840, ; 84: System.Globalization.Calendars => 0x20bbb280 => 40
	i32 557405415, ; 85: Jsr305Binding => 0x213954e7 => 275
	i32 569601784, ; 86: Xamarin.AndroidX.Window.Extensions.Core.Core => 0x21f36ef8 => 273
	i32 577335427, ; 87: System.Security.Cryptography.Cng => 0x22697083 => 120
	i32 601371474, ; 88: System.IO.IsolatedStorage.dll => 0x23d83352 => 52
	i32 605376203, ; 89: System.IO.Compression.FileSystem => 0x24154ecb => 44
	i32 613668793, ; 90: System.Security.Cryptography.Algorithms => 0x2493d7b9 => 119
	i32 627609679, ; 91: Xamarin.AndroidX.CustomView => 0x2568904f => 227
	i32 627931235, ; 92: nl\Microsoft.Maui.Controls.resources => 0x256d7863 => 305
	i32 639843206, ; 93: Xamarin.AndroidX.Emoji2.ViewsHelper.dll => 0x26233b86 => 233
	i32 643868501, ; 94: System.Net => 0x2660a755 => 81
	i32 646616860, ; 95: Microsoft.Web.WebView2.WinForms.dll => 0x268a971c => 321
	i32 662205335, ; 96: System.Text.Encodings.Web.dll => 0x27787397 => 136
	i32 663517072, ; 97: Xamarin.AndroidX.VersionedParcelable => 0x278c7790 => 269
	i32 666292255, ; 98: Xamarin.AndroidX.Arch.Core.Common.dll => 0x27b6d01f => 214
	i32 672442732, ; 99: System.Collections.Concurrent => 0x2814a96c => 8
	i32 683518922, ; 100: System.Net.Security => 0x28bdabca => 73
	i32 690569205, ; 101: System.Xml.Linq.dll => 0x29293ff5 => 155
	i32 691348768, ; 102: Xamarin.KotlinX.Coroutines.Android.dll => 0x29352520 => 284
	i32 693804605, ; 103: System.Windows => 0x295a9e3d => 154
	i32 699345723, ; 104: System.Reflection.Emit => 0x29af2b3b => 92
	i32 700284507, ; 105: Xamarin.Jetbrains.Annotations => 0x29bd7e5b => 279
	i32 700358131, ; 106: System.IO.Compression.ZipFile => 0x29be9df3 => 45
	i32 720511267, ; 107: Xamarin.Kotlin.StdLib.Jdk8 => 0x2af22123 => 283
	i32 722857257, ; 108: System.Runtime.Loader.dll => 0x2b15ed29 => 109
	i32 735137430, ; 109: System.Security.SecureString.dll => 0x2bd14e96 => 129
	i32 736260964, ; 110: LiveChartsCore.Behaviours => 0x2be27364 => 176
	i32 752232764, ; 111: System.Diagnostics.Contracts.dll => 0x2cd6293c => 25
	i32 755313932, ; 112: Xamarin.Android.Glide.Annotations.dll => 0x2d052d0c => 204
	i32 759454413, ; 113: System.Net.Requests => 0x2d445acd => 72
	i32 762598435, ; 114: System.IO.Pipes.dll => 0x2d745423 => 55
	i32 775507847, ; 115: System.IO.Compression => 0x2e394f87 => 46
	i32 777317022, ; 116: sk\Microsoft.Maui.Controls.resources => 0x2e54ea9e => 311
	i32 778756650, ; 117: SkiaSharp.HarfBuzz.dll => 0x2e6ae22a => 196
	i32 789151979, ; 118: Microsoft.Extensions.Options => 0x2f0980eb => 186
	i32 790371945, ; 119: Xamarin.AndroidX.CustomView.PoolingContainer.dll => 0x2f1c1e69 => 228
	i32 804715423, ; 120: System.Data.Common => 0x2ff6fb9f => 22
	i32 807930345, ; 121: Xamarin.AndroidX.Lifecycle.LiveData.Core.Ktx.dll => 0x302809e9 => 242
	i32 823281589, ; 122: System.Private.Uri.dll => 0x311247b5 => 86
	i32 830298997, ; 123: System.IO.Compression.Brotli => 0x317d5b75 => 43
	i32 832635846, ; 124: System.Xml.XPath.dll => 0x31a103c6 => 160
	i32 834051424, ; 125: System.Net.Quic => 0x31b69d60 => 71
	i32 843511501, ; 126: Xamarin.AndroidX.Print => 0x3246f6cd => 255
	i32 869139383, ; 127: hi\Microsoft.Maui.Controls.resources.dll => 0x33ce03b7 => 296
	i32 873119928, ; 128: Microsoft.VisualBasic => 0x340ac0b8 => 3
	i32 877678880, ; 129: System.Globalization.dll => 0x34505120 => 42
	i32 878954865, ; 130: System.Net.Http.Json => 0x3463c971 => 63
	i32 880668424, ; 131: ru\Microsoft.Maui.Controls.resources.dll => 0x347def08 => 310
	i32 904024072, ; 132: System.ComponentModel.Primitives.dll => 0x35e25008 => 16
	i32 911108515, ; 133: System.IO.MemoryMappedFiles.dll => 0x364e69a3 => 53
	i32 918734561, ; 134: pt-BR\Microsoft.Maui.Controls.resources.dll => 0x36c2c6e1 => 307
	i32 928116545, ; 135: Xamarin.Google.Guava.ListenableFuture => 0x3751ef41 => 278
	i32 952186615, ; 136: System.Runtime.InteropServices.JavaScript.dll => 0x38c136f7 => 105
	i32 956575887, ; 137: Xamarin.Kotlin.StdLib.Jdk8.dll => 0x3904308f => 283
	i32 961460050, ; 138: it\Microsoft.Maui.Controls.resources.dll => 0x394eb752 => 300
	i32 966729478, ; 139: Xamarin.Google.Crypto.Tink.Android => 0x399f1f06 => 276
	i32 967690846, ; 140: Xamarin.AndroidX.Lifecycle.Common.dll => 0x39adca5e => 239
	i32 975236339, ; 141: System.Diagnostics.Tracing => 0x3a20ecf3 => 34
	i32 975874589, ; 142: System.Xml.XDocument => 0x3a2aaa1d => 158
	i32 986514023, ; 143: System.Private.DataContractSerialization.dll => 0x3acd0267 => 85
	i32 987214855, ; 144: System.Diagnostics.Tools => 0x3ad7b407 => 32
	i32 990727110, ; 145: ro\Microsoft.Maui.Controls.resources.dll => 0x3b0d4bc6 => 309
	i32 992768348, ; 146: System.Collections.dll => 0x3b2c715c => 12
	i32 994442037, ; 147: System.IO.FileSystem => 0x3b45fb35 => 51
	i32 1001831731, ; 148: System.IO.UnmanagedMemoryStream.dll => 0x3bb6bd33 => 56
	i32 1012816738, ; 149: Xamarin.AndroidX.SavedState.dll => 0x3c5e5b62 => 259
	i32 1019214401, ; 150: System.Drawing => 0x3cbffa41 => 36
	i32 1028951442, ; 151: Microsoft.Extensions.DependencyInjection.Abstractions => 0x3d548d92 => 182
	i32 1031528504, ; 152: Xamarin.Google.ErrorProne.Annotations.dll => 0x3d7be038 => 277
	i32 1034083993, ; 153: LiveChartsCore.SkiaSharpView.Maui.dll => 0x3da2de99 => 178
	i32 1035644815, ; 154: Xamarin.AndroidX.AppCompat => 0x3dbaaf8f => 212
	i32 1036536393, ; 155: System.Drawing.Primitives.dll => 0x3dc84a49 => 35
	i32 1043950537, ; 156: de\Microsoft.Maui.Controls.resources.dll => 0x3e396bc9 => 290
	i32 1044663988, ; 157: System.Linq.Expressions.dll => 0x3e444eb4 => 58
	i32 1052210849, ; 158: Xamarin.AndroidX.Lifecycle.ViewModel.dll => 0x3eb776a1 => 246
	i32 1067306892, ; 159: GoogleGson => 0x3f9dcf8c => 173
	i32 1082857460, ; 160: System.ComponentModel.TypeConverter => 0x408b17f4 => 17
	i32 1084122840, ; 161: Xamarin.Kotlin.StdLib => 0x409e66d8 => 280
	i32 1098259244, ; 162: System => 0x41761b2c => 164
	i32 1108272742, ; 163: sv\Microsoft.Maui.Controls.resources.dll => 0x420ee666 => 312
	i32 1117529484, ; 164: pl\Microsoft.Maui.Controls.resources.dll => 0x429c258c => 306
	i32 1118262833, ; 165: ko\Microsoft.Maui.Controls.resources => 0x42a75631 => 302
	i32 1121599056, ; 166: Xamarin.AndroidX.Lifecycle.Runtime.Ktx.dll => 0x42da3e50 => 245
	i32 1127624469, ; 167: Microsoft.Extensions.Logging.Debug => 0x43362f15 => 185
	i32 1149092582, ; 168: Xamarin.AndroidX.Window => 0x447dc2e6 => 272
	i32 1168523401, ; 169: pt\Microsoft.Maui.Controls.resources => 0x45a64089 => 308
	i32 1170634674, ; 170: System.Web.dll => 0x45c677b2 => 153
	i32 1175144683, ; 171: Xamarin.AndroidX.VectorDrawable.Animated => 0x460b48eb => 268
	i32 1178241025, ; 172: Xamarin.AndroidX.Navigation.Runtime.dll => 0x463a8801 => 253
	i32 1204270330, ; 173: Xamarin.AndroidX.Arch.Core.Common => 0x47c7b4fa => 214
	i32 1208641965, ; 174: System.Diagnostics.Process => 0x480a69ad => 29
	i32 1219128291, ; 175: System.IO.IsolatedStorage => 0x48aa6be3 => 52
	i32 1243150071, ; 176: Xamarin.AndroidX.Window.Extensions.Core.Core.dll => 0x4a18f6f7 => 273
	i32 1253011324, ; 177: Microsoft.Win32.Registry => 0x4aaf6f7c => 5
	i32 1260983243, ; 178: cs\Microsoft.Maui.Controls.resources => 0x4b2913cb => 288
	i32 1264511973, ; 179: Xamarin.AndroidX.Startup.StartupRuntime.dll => 0x4b5eebe5 => 263
	i32 1267360935, ; 180: Xamarin.AndroidX.VectorDrawable => 0x4b8a64a7 => 267
	i32 1273260888, ; 181: Xamarin.AndroidX.Collection.Ktx => 0x4be46b58 => 219
	i32 1275534314, ; 182: Xamarin.KotlinX.Coroutines.Android => 0x4c071bea => 284
	i32 1278448581, ; 183: Xamarin.AndroidX.Annotation.Jvm => 0x4c3393c5 => 211
	i32 1283425954, ; 184: LiveChartsCore.SkiaSharpView => 0x4c7f86a2 => 177
	i32 1293217323, ; 185: Xamarin.AndroidX.DrawerLayout.dll => 0x4d14ee2b => 230
	i32 1308624726, ; 186: hr\Microsoft.Maui.Controls.resources.dll => 0x4e000756 => 297
	i32 1309188875, ; 187: System.Private.DataContractSerialization => 0x4e08a30b => 85
	i32 1322716291, ; 188: Xamarin.AndroidX.Window.dll => 0x4ed70c83 => 272
	i32 1324164729, ; 189: System.Linq => 0x4eed2679 => 61
	i32 1335329327, ; 190: System.Runtime.Serialization.Json.dll => 0x4f97822f => 112
	i32 1336711579, ; 191: zh-HK\Microsoft.Maui.Controls.resources.dll => 0x4fac999b => 317
	i32 1364015309, ; 192: System.IO => 0x514d38cd => 57
	i32 1373134921, ; 193: zh-Hans\Microsoft.Maui.Controls.resources => 0x51d86049 => 318
	i32 1376866003, ; 194: Xamarin.AndroidX.SavedState => 0x52114ed3 => 259
	i32 1379779777, ; 195: System.Resources.ResourceManager => 0x523dc4c1 => 99
	i32 1402170036, ; 196: System.Configuration.dll => 0x53936ab4 => 19
	i32 1406073936, ; 197: Xamarin.AndroidX.CoordinatorLayout => 0x53cefc50 => 223
	i32 1408764838, ; 198: System.Runtime.Serialization.Formatters.dll => 0x53f80ba6 => 111
	i32 1411638395, ; 199: System.Runtime.CompilerServices.Unsafe => 0x5423e47b => 101
	i32 1422545099, ; 200: System.Runtime.CompilerServices.VisualC => 0x54ca50cb => 102
	i32 1430672901, ; 201: ar\Microsoft.Maui.Controls.resources => 0x55465605 => 286
	i32 1434145427, ; 202: System.Runtime.Handles => 0x557b5293 => 104
	i32 1435222561, ; 203: Xamarin.Google.Crypto.Tink.Android.dll => 0x558bc221 => 276
	i32 1439761251, ; 204: System.Net.Quic.dll => 0x55d10363 => 71
	i32 1452070440, ; 205: System.Formats.Asn1.dll => 0x568cd628 => 38
	i32 1453312822, ; 206: System.Diagnostics.Tools.dll => 0x569fcb36 => 32
	i32 1457743152, ; 207: System.Runtime.Extensions.dll => 0x56e36530 => 103
	i32 1458022317, ; 208: System.Net.Security.dll => 0x56e7a7ad => 73
	i32 1461004990, ; 209: es\Microsoft.Maui.Controls.resources => 0x57152abe => 292
	i32 1461234159, ; 210: System.Collections.Immutable.dll => 0x5718a9ef => 9
	i32 1461719063, ; 211: System.Security.Cryptography.OpenSsl => 0x57201017 => 123
	i32 1462112819, ; 212: System.IO.Compression.dll => 0x57261233 => 46
	i32 1469204771, ; 213: Xamarin.AndroidX.AppCompat.AppCompatResources => 0x57924923 => 213
	i32 1470490898, ; 214: Microsoft.Extensions.Primitives => 0x57a5e912 => 187
	i32 1479771757, ; 215: System.Collections.Immutable => 0x5833866d => 9
	i32 1480492111, ; 216: System.IO.Compression.Brotli.dll => 0x583e844f => 43
	i32 1487239319, ; 217: Microsoft.Win32.Primitives => 0x58a57897 => 4
	i32 1490025113, ; 218: Xamarin.AndroidX.SavedState.SavedState.Ktx.dll => 0x58cffa99 => 260
	i32 1511525525, ; 219: MySqlConnector => 0x5a180c95 => 194
	i32 1526286932, ; 220: vi\Microsoft.Maui.Controls.resources.dll => 0x5af94a54 => 316
	i32 1536373174, ; 221: System.Diagnostics.TextWriterTraceListener => 0x5b9331b6 => 31
	i32 1543031311, ; 222: System.Text.RegularExpressions.dll => 0x5bf8ca0f => 138
	i32 1543355203, ; 223: System.Reflection.Emit.dll => 0x5bfdbb43 => 92
	i32 1550322496, ; 224: System.Reflection.Extensions.dll => 0x5c680b40 => 93
	i32 1565862583, ; 225: System.IO.FileSystem.Primitives => 0x5d552ab7 => 49
	i32 1566207040, ; 226: System.Threading.Tasks.Dataflow.dll => 0x5d5a6c40 => 141
	i32 1568197493, ; 227: Microsoft.Web.WebView2.Wpf.dll => 0x5d78cb75 => 322
	i32 1573704789, ; 228: System.Runtime.Serialization.Json => 0x5dccd455 => 112
	i32 1580037396, ; 229: System.Threading.Overlapped => 0x5e2d7514 => 140
	i32 1582372066, ; 230: Xamarin.AndroidX.DocumentFile.dll => 0x5e5114e2 => 229
	i32 1592978981, ; 231: System.Runtime.Serialization.dll => 0x5ef2ee25 => 115
	i32 1597949149, ; 232: Xamarin.Google.ErrorProne.Annotations => 0x5f3ec4dd => 277
	i32 1601112923, ; 233: System.Xml.Serialization => 0x5f6f0b5b => 157
	i32 1604827217, ; 234: System.Net.WebClient => 0x5fa7b851 => 76
	i32 1618516317, ; 235: System.Net.WebSockets.Client.dll => 0x6078995d => 79
	i32 1622152042, ; 236: Xamarin.AndroidX.Loader.dll => 0x60b0136a => 249
	i32 1622358360, ; 237: System.Dynamic.Runtime => 0x60b33958 => 37
	i32 1623212457, ; 238: SkiaSharp.Views.Maui.Controls => 0x60c041a9 => 198
	i32 1624863272, ; 239: Xamarin.AndroidX.ViewPager2 => 0x60d97228 => 271
	i32 1635184631, ; 240: Xamarin.AndroidX.Emoji2.ViewsHelper => 0x6176eff7 => 233
	i32 1636350590, ; 241: Xamarin.AndroidX.CursorAdapter => 0x6188ba7e => 226
	i32 1639515021, ; 242: System.Net.Http.dll => 0x61b9038d => 64
	i32 1639986890, ; 243: System.Text.RegularExpressions => 0x61c036ca => 138
	i32 1641389582, ; 244: System.ComponentModel.EventBasedAsync.dll => 0x61d59e0e => 15
	i32 1657153582, ; 245: System.Runtime => 0x62c6282e => 116
	i32 1658241508, ; 246: Xamarin.AndroidX.Tracing.Tracing.dll => 0x62d6c1e4 => 265
	i32 1658251792, ; 247: Xamarin.Google.Android.Material.dll => 0x62d6ea10 => 274
	i32 1670060433, ; 248: Xamarin.AndroidX.ConstraintLayout => 0x638b1991 => 221
	i32 1675553242, ; 249: System.IO.FileSystem.DriveInfo.dll => 0x63dee9da => 48
	i32 1677501392, ; 250: System.Net.Primitives.dll => 0x63fca3d0 => 70
	i32 1678508291, ; 251: System.Net.WebSockets => 0x640c0103 => 80
	i32 1679769178, ; 252: System.Security.Cryptography => 0x641f3e5a => 126
	i32 1691477237, ; 253: System.Reflection.Metadata => 0x64d1e4f5 => 94
	i32 1696967625, ; 254: System.Security.Cryptography.Csp => 0x6525abc9 => 121
	i32 1698840827, ; 255: Xamarin.Kotlin.StdLib.Common => 0x654240fb => 281
	i32 1700010563, ; 256: Microsoft.Web.WebView2.Core.dll => 0x65541a43 => 320
	i32 1701541528, ; 257: System.Diagnostics.Debug.dll => 0x656b7698 => 26
	i32 1715236781, ; 258: Microsoft.Web.WebView2.WinForms => 0x663c6fad => 321
	i32 1720223769, ; 259: Xamarin.AndroidX.Lifecycle.LiveData.Core.Ktx => 0x66888819 => 242
	i32 1726116996, ; 260: System.Reflection.dll => 0x66e27484 => 97
	i32 1728033016, ; 261: System.Diagnostics.FileVersionInfo.dll => 0x66ffb0f8 => 28
	i32 1729485958, ; 262: Xamarin.AndroidX.CardView.dll => 0x6715dc86 => 217
	i32 1743415430, ; 263: ca\Microsoft.Maui.Controls.resources => 0x67ea6886 => 287
	i32 1744735666, ; 264: System.Transactions.Local.dll => 0x67fe8db2 => 149
	i32 1746316138, ; 265: Mono.Android.Export => 0x6816ab6a => 169
	i32 1750313021, ; 266: Microsoft.Win32.Primitives.dll => 0x6853a83d => 4
	i32 1758240030, ; 267: System.Resources.Reader.dll => 0x68cc9d1e => 98
	i32 1763938596, ; 268: System.Diagnostics.TraceSource.dll => 0x69239124 => 33
	i32 1765942094, ; 269: System.Reflection.Extensions => 0x6942234e => 93
	i32 1766324549, ; 270: Xamarin.AndroidX.SwipeRefreshLayout => 0x6947f945 => 264
	i32 1770582343, ; 271: Microsoft.Extensions.Logging.dll => 0x6988f147 => 183
	i32 1776026572, ; 272: System.Core.dll => 0x69dc03cc => 21
	i32 1777075843, ; 273: System.Globalization.Extensions.dll => 0x69ec0683 => 41
	i32 1780572499, ; 274: Mono.Android.Runtime.dll => 0x6a216153 => 170
	i32 1782862114, ; 275: ms\Microsoft.Maui.Controls.resources => 0x6a445122 => 303
	i32 1788241197, ; 276: Xamarin.AndroidX.Fragment => 0x6a96652d => 235
	i32 1793755602, ; 277: he\Microsoft.Maui.Controls.resources => 0x6aea89d2 => 295
	i32 1808609942, ; 278: Xamarin.AndroidX.Loader => 0x6bcd3296 => 249
	i32 1813058853, ; 279: Xamarin.Kotlin.StdLib.dll => 0x6c111525 => 280
	i32 1813201214, ; 280: Xamarin.Google.Android.Material => 0x6c13413e => 274
	i32 1818569960, ; 281: Xamarin.AndroidX.Navigation.UI.dll => 0x6c652ce8 => 254
	i32 1818787751, ; 282: Microsoft.VisualBasic.Core => 0x6c687fa7 => 2
	i32 1824175904, ; 283: System.Text.Encoding.Extensions => 0x6cbab720 => 134
	i32 1824722060, ; 284: System.Runtime.Serialization.Formatters => 0x6cc30c8c => 111
	i32 1828688058, ; 285: Microsoft.Extensions.Logging.Abstractions.dll => 0x6cff90ba => 184
	i32 1847515442, ; 286: Xamarin.Android.Glide.Annotations => 0x6e1ed932 => 204
	i32 1853025655, ; 287: sv\Microsoft.Maui.Controls.resources => 0x6e72ed77 => 312
	i32 1858542181, ; 288: System.Linq.Expressions => 0x6ec71a65 => 58
	i32 1870277092, ; 289: System.Reflection.Primitives => 0x6f7a29e4 => 95
	i32 1875935024, ; 290: fr\Microsoft.Maui.Controls.resources => 0x6fd07f30 => 294
	i32 1879696579, ; 291: System.Formats.Tar.dll => 0x7009e4c3 => 39
	i32 1885316902, ; 292: Xamarin.AndroidX.Arch.Core.Runtime.dll => 0x705fa726 => 215
	i32 1888955245, ; 293: System.Diagnostics.Contracts => 0x70972b6d => 25
	i32 1889954781, ; 294: System.Reflection.Metadata.dll => 0x70a66bdd => 94
	i32 1893218855, ; 295: cs\Microsoft.Maui.Controls.resources.dll => 0x70d83a27 => 288
	i32 1898237753, ; 296: System.Reflection.DispatchProxy => 0x7124cf39 => 89
	i32 1900610850, ; 297: System.Resources.ResourceManager.dll => 0x71490522 => 99
	i32 1910275211, ; 298: System.Collections.NonGeneric.dll => 0x71dc7c8b => 10
	i32 1939592360, ; 299: System.Private.Xml.Linq => 0x739bd4a8 => 87
	i32 1953182387, ; 300: id\Microsoft.Maui.Controls.resources.dll => 0x746b32b3 => 299
	i32 1956758971, ; 301: System.Resources.Writer => 0x74a1c5bb => 100
	i32 1961813231, ; 302: Xamarin.AndroidX.Security.SecurityCrypto.dll => 0x74eee4ef => 261
	i32 1968388702, ; 303: Microsoft.Extensions.Configuration.dll => 0x75533a5e => 179
	i32 1983156543, ; 304: Xamarin.Kotlin.StdLib.Common.dll => 0x7634913f => 281
	i32 1985761444, ; 305: Xamarin.Android.Glide.GifDecoder => 0x765c50a4 => 206
	i32 2003115576, ; 306: el\Microsoft.Maui.Controls.resources => 0x77651e38 => 291
	i32 2011961780, ; 307: System.Buffers.dll => 0x77ec19b4 => 7
	i32 2019465201, ; 308: Xamarin.AndroidX.Lifecycle.ViewModel => 0x785e97f1 => 246
	i32 2031763787, ; 309: Xamarin.Android.Glide => 0x791a414b => 203
	i32 2045470958, ; 310: System.Private.Xml => 0x79eb68ee => 88
	i32 2055257422, ; 311: Xamarin.AndroidX.Lifecycle.LiveData.Core.dll => 0x7a80bd4e => 241
	i32 2060060697, ; 312: System.Windows.dll => 0x7aca0819 => 154
	i32 2066184531, ; 313: de\Microsoft.Maui.Controls.resources => 0x7b277953 => 290
	i32 2070888862, ; 314: System.Diagnostics.TraceSource => 0x7b6f419e => 33
	i32 2079903147, ; 315: System.Runtime.dll => 0x7bf8cdab => 116
	i32 2090596640, ; 316: System.Numerics.Vectors => 0x7c9bf920 => 82
	i32 2127167465, ; 317: System.Console => 0x7ec9ffe9 => 20
	i32 2142473426, ; 318: System.Collections.Specialized => 0x7fb38cd2 => 11
	i32 2143790110, ; 319: System.Xml.XmlSerializer.dll => 0x7fc7a41e => 162
	i32 2146852085, ; 320: Microsoft.VisualBasic.dll => 0x7ff65cf5 => 3
	i32 2159891885, ; 321: Microsoft.Maui => 0x80bd55ad => 191
	i32 2169148018, ; 322: hu\Microsoft.Maui.Controls.resources => 0x814a9272 => 298
	i32 2181898931, ; 323: Microsoft.Extensions.Options.dll => 0x820d22b3 => 186
	i32 2192057212, ; 324: Microsoft.Extensions.Logging.Abstractions => 0x82a8237c => 184
	i32 2193016926, ; 325: System.ObjectModel.dll => 0x82b6c85e => 84
	i32 2201107256, ; 326: Xamarin.KotlinX.Coroutines.Core.Jvm.dll => 0x83323b38 => 285
	i32 2201231467, ; 327: System.Net.Http => 0x8334206b => 64
	i32 2207618523, ; 328: it\Microsoft.Maui.Controls.resources => 0x839595db => 300
	i32 2217644978, ; 329: Xamarin.AndroidX.VectorDrawable.Animated.dll => 0x842e93b2 => 268
	i32 2222056684, ; 330: System.Threading.Tasks.Parallel => 0x8471e4ec => 143
	i32 2244775296, ; 331: Xamarin.AndroidX.LocalBroadcastManager => 0x85cc8d80 => 250
	i32 2252106437, ; 332: System.Xml.Serialization.dll => 0x863c6ac5 => 157
	i32 2256313426, ; 333: System.Globalization.Extensions => 0x867c9c52 => 41
	i32 2265110946, ; 334: System.Security.AccessControl.dll => 0x8702d9a2 => 117
	i32 2266799131, ; 335: Microsoft.Extensions.Configuration.Abstractions => 0x871c9c1b => 180
	i32 2267999099, ; 336: Xamarin.Android.Glide.DiskLruCache.dll => 0x872eeb7b => 205
	i32 2279755925, ; 337: Xamarin.AndroidX.RecyclerView.dll => 0x87e25095 => 257
	i32 2293034957, ; 338: System.ServiceModel.Web.dll => 0x88acefcd => 131
	i32 2295906218, ; 339: System.Net.Sockets => 0x88d8bfaa => 75
	i32 2298471582, ; 340: System.Net.Mail => 0x88ffe49e => 66
	i32 2303942373, ; 341: nb\Microsoft.Maui.Controls.resources => 0x89535ee5 => 304
	i32 2305521784, ; 342: System.Private.CoreLib.dll => 0x896b7878 => 172
	i32 2315684594, ; 343: Xamarin.AndroidX.Annotation.dll => 0x8a068af2 => 209
	i32 2320631194, ; 344: System.Threading.Tasks.Parallel.dll => 0x8a52059a => 143
	i32 2340441535, ; 345: System.Runtime.InteropServices.RuntimeInformation.dll => 0x8b804dbf => 106
	i32 2344264397, ; 346: System.ValueTuple => 0x8bbaa2cd => 151
	i32 2353062107, ; 347: System.Net.Primitives => 0x8c40e0db => 70
	i32 2354730003, ; 348: Syncfusion.Licensing => 0x8c5a5413 => 200
	i32 2364201794, ; 349: SkiaSharp.Views.Maui.Core => 0x8ceadb42 => 199
	i32 2366048013, ; 350: hu\Microsoft.Maui.Controls.resources.dll => 0x8d07070d => 298
	i32 2368005991, ; 351: System.Xml.ReaderWriter.dll => 0x8d24e767 => 156
	i32 2371007202, ; 352: Microsoft.Extensions.Configuration => 0x8d52b2e2 => 179
	i32 2378619854, ; 353: System.Security.Cryptography.Csp.dll => 0x8dc6dbce => 121
	i32 2383496789, ; 354: System.Security.Principal.Windows.dll => 0x8e114655 => 127
	i32 2395872292, ; 355: id\Microsoft.Maui.Controls.resources => 0x8ece1c24 => 299
	i32 2401565422, ; 356: System.Web.HttpUtility => 0x8f24faee => 152
	i32 2403452196, ; 357: Xamarin.AndroidX.Emoji2.dll => 0x8f41c524 => 232
	i32 2404280560, ; 358: CorePlan.dll => 0x8f4e68f0 => 0
	i32 2421380589, ; 359: System.Threading.Tasks.Dataflow => 0x905355ed => 141
	i32 2423080555, ; 360: Xamarin.AndroidX.Collection.Ktx.dll => 0x906d466b => 219
	i32 2427813419, ; 361: hi\Microsoft.Maui.Controls.resources => 0x90b57e2b => 296
	i32 2435356389, ; 362: System.Console.dll => 0x912896e5 => 20
	i32 2435904999, ; 363: System.ComponentModel.DataAnnotations.dll => 0x9130f5e7 => 14
	i32 2454642406, ; 364: System.Text.Encoding.dll => 0x924edee6 => 135
	i32 2458678730, ; 365: System.Net.Sockets.dll => 0x928c75ca => 75
	i32 2459001652, ; 366: System.Linq.Parallel.dll => 0x92916334 => 59
	i32 2465532216, ; 367: Xamarin.AndroidX.ConstraintLayout.Core.dll => 0x92f50938 => 222
	i32 2471841756, ; 368: netstandard.dll => 0x93554fdc => 167
	i32 2475788418, ; 369: Java.Interop.dll => 0x93918882 => 168
	i32 2480646305, ; 370: Microsoft.Maui.Controls => 0x93dba8a1 => 189
	i32 2483903535, ; 371: System.ComponentModel.EventBasedAsync => 0x940d5c2f => 15
	i32 2484371297, ; 372: System.Net.ServicePoint => 0x94147f61 => 74
	i32 2490993605, ; 373: System.AppContext.dll => 0x94798bc5 => 6
	i32 2501346920, ; 374: System.Data.DataSetExtensions => 0x95178668 => 23
	i32 2503351294, ; 375: ko\Microsoft.Maui.Controls.resources.dll => 0x95361bfe => 302
	i32 2505896520, ; 376: Xamarin.AndroidX.Lifecycle.Runtime.dll => 0x955cf248 => 244
	i32 2522472828, ; 377: Xamarin.Android.Glide.dll => 0x9659e17c => 203
	i32 2538310050, ; 378: System.Reflection.Emit.Lightweight.dll => 0x974b89a2 => 91
	i32 2550873716, ; 379: hr\Microsoft.Maui.Controls.resources => 0x980b3e74 => 297
	i32 2556439392, ; 380: LiveChartsCore.SkiaSharpView.Maui => 0x98602b60 => 178
	i32 2562349572, ; 381: Microsoft.CSharp => 0x98ba5a04 => 1
	i32 2570120770, ; 382: System.Text.Encodings.Web => 0x9930ee42 => 136
	i32 2576534780, ; 383: ja\Microsoft.Maui.Controls.resources.dll => 0x9992ccfc => 301
	i32 2581783588, ; 384: Xamarin.AndroidX.Lifecycle.Runtime.Ktx => 0x99e2e424 => 245
	i32 2581819634, ; 385: Xamarin.AndroidX.VectorDrawable.dll => 0x99e370f2 => 267
	i32 2585220780, ; 386: System.Text.Encoding.Extensions.dll => 0x9a1756ac => 134
	i32 2585805581, ; 387: System.Net.Ping => 0x9a20430d => 69
	i32 2589602615, ; 388: System.Threading.ThreadPool => 0x9a5a3337 => 146
	i32 2593496499, ; 389: pl\Microsoft.Maui.Controls.resources => 0x9a959db3 => 306
	i32 2605712449, ; 390: Xamarin.KotlinX.Coroutines.Core.Jvm => 0x9b500441 => 285
	i32 2615233544, ; 391: Xamarin.AndroidX.Fragment.Ktx => 0x9be14c08 => 236
	i32 2616218305, ; 392: Microsoft.Extensions.Logging.Debug.dll => 0x9bf052c1 => 185
	i32 2617129537, ; 393: System.Private.Xml.dll => 0x9bfe3a41 => 88
	i32 2618712057, ; 394: System.Reflection.TypeExtensions.dll => 0x9c165ff9 => 96
	i32 2620871830, ; 395: Xamarin.AndroidX.CursorAdapter.dll => 0x9c375496 => 226
	i32 2624644809, ; 396: Xamarin.AndroidX.DynamicAnimation => 0x9c70e6c9 => 231
	i32 2625339995, ; 397: SkiaSharp.Views.Maui.Core.dll => 0x9c7b825b => 199
	i32 2626831493, ; 398: ja\Microsoft.Maui.Controls.resources => 0x9c924485 => 301
	i32 2627185994, ; 399: System.Diagnostics.TextWriterTraceListener.dll => 0x9c97ad4a => 31
	i32 2629843544, ; 400: System.IO.Compression.ZipFile.dll => 0x9cc03a58 => 45
	i32 2633051222, ; 401: Xamarin.AndroidX.Lifecycle.LiveData => 0x9cf12c56 => 240
	i32 2658541417, ; 402: Microsoft.Web.WebView2.Wpf => 0x9e761f69 => 322
	i32 2663391936, ; 403: Xamarin.Android.Glide.DiskLruCache => 0x9ec022c0 => 205
	i32 2663698177, ; 404: System.Runtime.Loader => 0x9ec4cf01 => 109
	i32 2664396074, ; 405: System.Xml.XDocument.dll => 0x9ecf752a => 158
	i32 2665622720, ; 406: System.Drawing.Primitives => 0x9ee22cc0 => 35
	i32 2676780864, ; 407: System.Data.Common.dll => 0x9f8c6f40 => 22
	i32 2686887180, ; 408: System.Runtime.Serialization.Xml.dll => 0xa026a50c => 114
	i32 2693849962, ; 409: System.IO.dll => 0xa090e36a => 57
	i32 2701096212, ; 410: Xamarin.AndroidX.Tracing.Tracing => 0xa0ff7514 => 265
	i32 2715334215, ; 411: System.Threading.Tasks.dll => 0xa1d8b647 => 144
	i32 2717744543, ; 412: System.Security.Claims => 0xa1fd7d9f => 118
	i32 2719963679, ; 413: System.Security.Cryptography.Cng.dll => 0xa21f5a1f => 120
	i32 2724373263, ; 414: System.Runtime.Numerics.dll => 0xa262a30f => 110
	i32 2732626843, ; 415: Xamarin.AndroidX.Activity => 0xa2e0939b => 207
	i32 2735172069, ; 416: System.Threading.Channels => 0xa30769e5 => 139
	i32 2737747696, ; 417: Xamarin.AndroidX.AppCompat.AppCompatResources.dll => 0xa32eb6f0 => 213
	i32 2740698338, ; 418: ca\Microsoft.Maui.Controls.resources.dll => 0xa35bbce2 => 287
	i32 2740948882, ; 419: System.IO.Pipes.AccessControl => 0xa35f8f92 => 54
	i32 2748088231, ; 420: System.Runtime.InteropServices.JavaScript => 0xa3cc7fa7 => 105
	i32 2752995522, ; 421: pt-BR\Microsoft.Maui.Controls.resources => 0xa41760c2 => 307
	i32 2758225723, ; 422: Microsoft.Maui.Controls.Xaml => 0xa4672f3b => 190
	i32 2764765095, ; 423: Microsoft.Maui.dll => 0xa4caf7a7 => 191
	i32 2765824710, ; 424: System.Text.Encoding.CodePages.dll => 0xa4db22c6 => 133
	i32 2770495804, ; 425: Xamarin.Jetbrains.Annotations.dll => 0xa522693c => 279
	i32 2778768386, ; 426: Xamarin.AndroidX.ViewPager.dll => 0xa5a0a402 => 270
	i32 2779977773, ; 427: Xamarin.AndroidX.ResourceInspection.Annotation.dll => 0xa5b3182d => 258
	i32 2785988530, ; 428: th\Microsoft.Maui.Controls.resources => 0xa60ecfb2 => 313
	i32 2788224221, ; 429: Xamarin.AndroidX.Fragment.Ktx.dll => 0xa630ecdd => 236
	i32 2795602088, ; 430: SkiaSharp.Views.Android.dll => 0xa6a180a8 => 197
	i32 2801831435, ; 431: Microsoft.Maui.Graphics => 0xa7008e0b => 193
	i32 2803228030, ; 432: System.Xml.XPath.XDocument.dll => 0xa715dd7e => 159
	i32 2810250172, ; 433: Xamarin.AndroidX.CoordinatorLayout.dll => 0xa78103bc => 223
	i32 2819470561, ; 434: System.Xml.dll => 0xa80db4e1 => 163
	i32 2821205001, ; 435: System.ServiceProcess.dll => 0xa8282c09 => 132
	i32 2821294376, ; 436: Xamarin.AndroidX.ResourceInspection.Annotation => 0xa8298928 => 258
	i32 2824502124, ; 437: System.Xml.XmlDocument => 0xa85a7b6c => 161
	i32 2838993487, ; 438: Xamarin.AndroidX.Lifecycle.ViewModel.Ktx.dll => 0xa9379a4f => 247
	i32 2849599387, ; 439: System.Threading.Overlapped.dll => 0xa9d96f9b => 140
	i32 2853208004, ; 440: Xamarin.AndroidX.ViewPager => 0xaa107fc4 => 270
	i32 2855708567, ; 441: Xamarin.AndroidX.Transition => 0xaa36a797 => 266
	i32 2861098320, ; 442: Mono.Android.Export.dll => 0xaa88e550 => 169
	i32 2861189240, ; 443: Microsoft.Maui.Essentials => 0xaa8a4878 => 192
	i32 2868557005, ; 444: Syncfusion.Licensing.dll => 0xaafab4cd => 200
	i32 2870099610, ; 445: Xamarin.AndroidX.Activity.Ktx.dll => 0xab123e9a => 208
	i32 2875164099, ; 446: Jsr305Binding.dll => 0xab5f85c3 => 275
	i32 2875220617, ; 447: System.Globalization.Calendars.dll => 0xab606289 => 40
	i32 2884993177, ; 448: Xamarin.AndroidX.ExifInterface => 0xabf58099 => 234
	i32 2887636118, ; 449: System.Net.dll => 0xac1dd496 => 81
	i32 2899753641, ; 450: System.IO.UnmanagedMemoryStream => 0xacd6baa9 => 56
	i32 2900621748, ; 451: System.Dynamic.Runtime.dll => 0xace3f9b4 => 37
	i32 2901442782, ; 452: System.Reflection => 0xacf080de => 97
	i32 2905242038, ; 453: mscorlib.dll => 0xad2a79b6 => 166
	i32 2909740682, ; 454: System.Private.CoreLib => 0xad6f1e8a => 172
	i32 2912489636, ; 455: SkiaSharp.Views.Android => 0xad9910a4 => 197
	i32 2916838712, ; 456: Xamarin.AndroidX.ViewPager2.dll => 0xaddb6d38 => 271
	i32 2919462931, ; 457: System.Numerics.Vectors.dll => 0xae037813 => 82
	i32 2921128767, ; 458: Xamarin.AndroidX.Annotation.Experimental.dll => 0xae1ce33f => 210
	i32 2936416060, ; 459: System.Resources.Reader => 0xaf06273c => 98
	i32 2940926066, ; 460: System.Diagnostics.StackTrace.dll => 0xaf4af872 => 30
	i32 2942453041, ; 461: System.Xml.XPath.XDocument => 0xaf624531 => 159
	i32 2959614098, ; 462: System.ComponentModel.dll => 0xb0682092 => 18
	i32 2968338931, ; 463: System.Security.Principal.Windows => 0xb0ed41f3 => 127
	i32 2972252294, ; 464: System.Security.Cryptography.Algorithms.dll => 0xb128f886 => 119
	i32 2978675010, ; 465: Xamarin.AndroidX.DrawerLayout => 0xb18af942 => 230
	i32 2987532451, ; 466: Xamarin.AndroidX.Security.SecurityCrypto => 0xb21220a3 => 261
	i32 2996846495, ; 467: Xamarin.AndroidX.Lifecycle.Process.dll => 0xb2a03f9f => 243
	i32 3016983068, ; 468: Xamarin.AndroidX.Startup.StartupRuntime => 0xb3d3821c => 263
	i32 3023353419, ; 469: WindowsBase.dll => 0xb434b64b => 165
	i32 3024354802, ; 470: Xamarin.AndroidX.Legacy.Support.Core.Utils => 0xb443fdf2 => 238
	i32 3038032645, ; 471: _Microsoft.Android.Resource.Designer.dll => 0xb514b305 => 323
	i32 3053864966, ; 472: fi\Microsoft.Maui.Controls.resources.dll => 0xb6064806 => 293
	i32 3056245963, ; 473: Xamarin.AndroidX.SavedState.SavedState.Ktx => 0xb62a9ccb => 260
	i32 3057625584, ; 474: Xamarin.AndroidX.Navigation.Common => 0xb63fa9f0 => 251
	i32 3059408633, ; 475: Mono.Android.Runtime => 0xb65adef9 => 170
	i32 3059793426, ; 476: System.ComponentModel.Primitives => 0xb660be12 => 16
	i32 3075834255, ; 477: System.Threading.Tasks => 0xb755818f => 144
	i32 3081706019, ; 478: LiveChartsCore => 0xb7af1a23 => 175
	i32 3090735792, ; 479: System.Security.Cryptography.X509Certificates.dll => 0xb838e2b0 => 125
	i32 3099732863, ; 480: System.Security.Claims.dll => 0xb8c22b7f => 118
	i32 3103600923, ; 481: System.Formats.Asn1 => 0xb8fd311b => 38
	i32 3111772706, ; 482: System.Runtime.Serialization => 0xb979e222 => 115
	i32 3121463068, ; 483: System.IO.FileSystem.AccessControl.dll => 0xba0dbf1c => 47
	i32 3124832203, ; 484: System.Threading.Tasks.Extensions => 0xba4127cb => 142
	i32 3132293585, ; 485: System.Security.AccessControl => 0xbab301d1 => 117
	i32 3147165239, ; 486: System.Diagnostics.Tracing.dll => 0xbb95ee37 => 34
	i32 3147228406, ; 487: Syncfusion.Maui.Core => 0xbb96e4f6 => 202
	i32 3148237826, ; 488: GoogleGson.dll => 0xbba64c02 => 173
	i32 3159123045, ; 489: System.Reflection.Primitives.dll => 0xbc4c6465 => 95
	i32 3160747431, ; 490: System.IO.MemoryMappedFiles => 0xbc652da7 => 53
	i32 3178803400, ; 491: Xamarin.AndroidX.Navigation.Fragment.dll => 0xbd78b0c8 => 252
	i32 3192346100, ; 492: System.Security.SecureString => 0xbe4755f4 => 129
	i32 3193515020, ; 493: System.Web => 0xbe592c0c => 153
	i32 3204380047, ; 494: System.Data.dll => 0xbefef58f => 24
	i32 3209718065, ; 495: System.Xml.XmlDocument.dll => 0xbf506931 => 161
	i32 3211777861, ; 496: Xamarin.AndroidX.DocumentFile => 0xbf6fd745 => 229
	i32 3220365878, ; 497: System.Threading => 0xbff2e236 => 148
	i32 3226221578, ; 498: System.Runtime.Handles.dll => 0xc04c3c0a => 104
	i32 3245644316, ; 499: Syncfusion.Maui.Charts.dll => 0xc1749a1c => 201
	i32 3251039220, ; 500: System.Reflection.DispatchProxy.dll => 0xc1c6ebf4 => 89
	i32 3258312781, ; 501: Xamarin.AndroidX.CardView => 0xc235e84d => 217
	i32 3265493905, ; 502: System.Linq.Queryable.dll => 0xc2a37b91 => 60
	i32 3265893370, ; 503: System.Threading.Tasks.Extensions.dll => 0xc2a993fa => 142
	i32 3277815716, ; 504: System.Resources.Writer.dll => 0xc35f7fa4 => 100
	i32 3279906254, ; 505: Microsoft.Win32.Registry.dll => 0xc37f65ce => 5
	i32 3280506390, ; 506: System.ComponentModel.Annotations.dll => 0xc3888e16 => 13
	i32 3290767353, ; 507: System.Security.Cryptography.Encoding => 0xc4251ff9 => 122
	i32 3299363146, ; 508: System.Text.Encoding => 0xc4a8494a => 135
	i32 3303498502, ; 509: System.Diagnostics.FileVersionInfo => 0xc4e76306 => 28
	i32 3305363605, ; 510: fi\Microsoft.Maui.Controls.resources => 0xc503d895 => 293
	i32 3316684772, ; 511: System.Net.Requests.dll => 0xc5b097e4 => 72
	i32 3317135071, ; 512: Xamarin.AndroidX.CustomView.dll => 0xc5b776df => 227
	i32 3317144872, ; 513: System.Data => 0xc5b79d28 => 24
	i32 3340387945, ; 514: SkiaSharp => 0xc71a4669 => 195
	i32 3340431453, ; 515: Xamarin.AndroidX.Arch.Core.Runtime => 0xc71af05d => 215
	i32 3345895724, ; 516: Xamarin.AndroidX.ProfileInstaller.ProfileInstaller.dll => 0xc76e512c => 256
	i32 3346324047, ; 517: Xamarin.AndroidX.Navigation.Runtime => 0xc774da4f => 253
	i32 3357674450, ; 518: ru\Microsoft.Maui.Controls.resources => 0xc8220bd2 => 310
	i32 3358260929, ; 519: System.Text.Json => 0xc82afec1 => 137
	i32 3362336904, ; 520: Xamarin.AndroidX.Activity.Ktx => 0xc8693088 => 208
	i32 3362522851, ; 521: Xamarin.AndroidX.Core => 0xc86c06e3 => 224
	i32 3366347497, ; 522: Java.Interop => 0xc8a662e9 => 168
	i32 3374999561, ; 523: Xamarin.AndroidX.RecyclerView => 0xc92a6809 => 257
	i32 3381016424, ; 524: da\Microsoft.Maui.Controls.resources => 0xc9863768 => 289
	i32 3384551493, ; 525: LiveChartsCore.dll => 0xc9bc2845 => 175
	i32 3395150330, ; 526: System.Runtime.CompilerServices.Unsafe.dll => 0xca5de1fa => 101
	i32 3403906625, ; 527: System.Security.Cryptography.OpenSsl.dll => 0xcae37e41 => 123
	i32 3405233483, ; 528: Xamarin.AndroidX.CustomView.PoolingContainer => 0xcaf7bd4b => 228
	i32 3428513518, ; 529: Microsoft.Extensions.DependencyInjection.dll => 0xcc5af6ee => 181
	i32 3429136800, ; 530: System.Xml => 0xcc6479a0 => 163
	i32 3430777524, ; 531: netstandard => 0xcc7d82b4 => 167
	i32 3441283291, ; 532: Xamarin.AndroidX.DynamicAnimation.dll => 0xcd1dd0db => 231
	i32 3445260447, ; 533: System.Formats.Tar => 0xcd5a809f => 39
	i32 3452344032, ; 534: Microsoft.Maui.Controls.Compatibility.dll => 0xcdc696e0 => 188
	i32 3458724246, ; 535: pt\Microsoft.Maui.Controls.resources.dll => 0xce27f196 => 308
	i32 3471940407, ; 536: System.ComponentModel.TypeConverter.dll => 0xcef19b37 => 17
	i32 3473156932, ; 537: SkiaSharp.Views.Maui.Controls.dll => 0xcf042b44 => 198
	i32 3476120550, ; 538: Mono.Android => 0xcf3163e6 => 171
	i32 3484440000, ; 539: ro\Microsoft.Maui.Controls.resources => 0xcfb055c0 => 309
	i32 3485117614, ; 540: System.Text.Json.dll => 0xcfbaacae => 137
	i32 3486566296, ; 541: System.Transactions => 0xcfd0c798 => 150
	i32 3493954962, ; 542: Xamarin.AndroidX.Concurrent.Futures.dll => 0xd0418592 => 220
	i32 3505680818, ; 543: CorePlan => 0xd0f471b2 => 0
	i32 3507431746, ; 544: Microsoft.Web.WebView2.Core => 0xd10f2942 => 320
	i32 3509114376, ; 545: System.Xml.Linq => 0xd128d608 => 155
	i32 3515174580, ; 546: System.Security.dll => 0xd1854eb4 => 130
	i32 3530912306, ; 547: System.Configuration => 0xd2757232 => 19
	i32 3539954161, ; 548: System.Net.HttpListener => 0xd2ff69f1 => 65
	i32 3556829416, ; 549: LiveChartsCore.Behaviours.dll => 0xd400e8e8 => 176
	i32 3560100363, ; 550: System.Threading.Timer => 0xd432d20b => 147
	i32 3570554715, ; 551: System.IO.FileSystem.AccessControl => 0xd4d2575b => 47
	i32 3580758918, ; 552: zh-HK\Microsoft.Maui.Controls.resources => 0xd56e0b86 => 317
	i32 3592228221, ; 553: zh-Hant\Microsoft.Maui.Controls.resources.dll => 0xd61d0d7d => 319
	i32 3597029428, ; 554: Xamarin.Android.Glide.GifDecoder.dll => 0xd6665034 => 206
	i32 3598340787, ; 555: System.Net.WebSockets.Client => 0xd67a52b3 => 79
	i32 3608519521, ; 556: System.Linq.dll => 0xd715a361 => 61
	i32 3624195450, ; 557: System.Runtime.InteropServices.RuntimeInformation => 0xd804d57a => 106
	i32 3627220390, ; 558: Xamarin.AndroidX.Print.dll => 0xd832fda6 => 255
	i32 3633644679, ; 559: Xamarin.AndroidX.Annotation.Experimental => 0xd8950487 => 210
	i32 3638274909, ; 560: System.IO.FileSystem.Primitives.dll => 0xd8dbab5d => 49
	i32 3641597786, ; 561: Xamarin.AndroidX.Lifecycle.LiveData.Core => 0xd90e5f5a => 241
	i32 3643446276, ; 562: tr\Microsoft.Maui.Controls.resources => 0xd92a9404 => 314
	i32 3643854240, ; 563: Xamarin.AndroidX.Navigation.Fragment => 0xd930cda0 => 252
	i32 3645089577, ; 564: System.ComponentModel.DataAnnotations => 0xd943a729 => 14
	i32 3657292374, ; 565: Microsoft.Extensions.Configuration.Abstractions.dll => 0xd9fdda56 => 180
	i32 3660523487, ; 566: System.Net.NetworkInformation => 0xda2f27df => 68
	i32 3672681054, ; 567: Mono.Android.dll => 0xdae8aa5e => 171
	i32 3682565725, ; 568: Xamarin.AndroidX.Browser => 0xdb7f7e5d => 216
	i32 3684561358, ; 569: Xamarin.AndroidX.Concurrent.Futures => 0xdb9df1ce => 220
	i32 3700866549, ; 570: System.Net.WebProxy.dll => 0xdc96bdf5 => 78
	i32 3706696989, ; 571: Xamarin.AndroidX.Core.Core.Ktx.dll => 0xdcefb51d => 225
	i32 3716563718, ; 572: System.Runtime.Intrinsics => 0xdd864306 => 108
	i32 3718780102, ; 573: Xamarin.AndroidX.Annotation => 0xdda814c6 => 209
	i32 3724971120, ; 574: Xamarin.AndroidX.Navigation.Common.dll => 0xde068c70 => 251
	i32 3732100267, ; 575: System.Net.NameResolution => 0xde7354ab => 67
	i32 3737834244, ; 576: System.Net.Http.Json.dll => 0xdecad304 => 63
	i32 3748608112, ; 577: System.Diagnostics.DiagnosticSource => 0xdf6f3870 => 27
	i32 3751444290, ; 578: System.Xml.XPath => 0xdf9a7f42 => 160
	i32 3751619990, ; 579: da\Microsoft.Maui.Controls.resources.dll => 0xdf9d2d96 => 289
	i32 3786282454, ; 580: Xamarin.AndroidX.Collection => 0xe1ae15d6 => 218
	i32 3792276235, ; 581: System.Collections.NonGeneric => 0xe2098b0b => 10
	i32 3792835768, ; 582: HarfBuzzSharp => 0xe21214b8 => 174
	i32 3800979733, ; 583: Microsoft.Maui.Controls.Compatibility => 0xe28e5915 => 188
	i32 3802395368, ; 584: System.Collections.Specialized.dll => 0xe2a3f2e8 => 11
	i32 3819260425, ; 585: System.Net.WebProxy => 0xe3a54a09 => 78
	i32 3823082795, ; 586: System.Security.Cryptography.dll => 0xe3df9d2b => 126
	i32 3829621856, ; 587: System.Numerics.dll => 0xe4436460 => 83
	i32 3841636137, ; 588: Microsoft.Extensions.DependencyInjection.Abstractions.dll => 0xe4fab729 => 182
	i32 3844307129, ; 589: System.Net.Mail.dll => 0xe52378b9 => 66
	i32 3849253459, ; 590: System.Runtime.InteropServices.dll => 0xe56ef253 => 107
	i32 3870376305, ; 591: System.Net.HttpListener.dll => 0xe6b14171 => 65
	i32 3873536506, ; 592: System.Security.Principal => 0xe6e179fa => 128
	i32 3875112723, ; 593: System.Security.Cryptography.Encoding.dll => 0xe6f98713 => 122
	i32 3885497537, ; 594: System.Net.WebHeaderCollection.dll => 0xe797fcc1 => 77
	i32 3885922214, ; 595: Xamarin.AndroidX.Transition.dll => 0xe79e77a6 => 266
	i32 3888767677, ; 596: Xamarin.AndroidX.ProfileInstaller.ProfileInstaller => 0xe7c9e2bd => 256
	i32 3896106733, ; 597: System.Collections.Concurrent.dll => 0xe839deed => 8
	i32 3896760992, ; 598: Xamarin.AndroidX.Core.dll => 0xe843daa0 => 224
	i32 3901907137, ; 599: Microsoft.VisualBasic.Core.dll => 0xe89260c1 => 2
	i32 3920221145, ; 600: nl\Microsoft.Maui.Controls.resources.dll => 0xe9a9d3d9 => 305
	i32 3920810846, ; 601: System.IO.Compression.FileSystem.dll => 0xe9b2d35e => 44
	i32 3921031405, ; 602: Xamarin.AndroidX.VersionedParcelable.dll => 0xe9b630ed => 269
	i32 3928044579, ; 603: System.Xml.ReaderWriter => 0xea213423 => 156
	i32 3930554604, ; 604: System.Security.Principal.dll => 0xea4780ec => 128
	i32 3931092270, ; 605: Xamarin.AndroidX.Navigation.UI => 0xea4fb52e => 254
	i32 3945713374, ; 606: System.Data.DataSetExtensions.dll => 0xeb2ecede => 23
	i32 3953953790, ; 607: System.Text.Encoding.CodePages => 0xebac8bfe => 133
	i32 3955647286, ; 608: Xamarin.AndroidX.AppCompat.dll => 0xebc66336 => 212
	i32 3959773229, ; 609: Xamarin.AndroidX.Lifecycle.Process => 0xec05582d => 243
	i32 4003436829, ; 610: System.Diagnostics.Process.dll => 0xee9f991d => 29
	i32 4003906742, ; 611: HarfBuzzSharp.dll => 0xeea6c4b6 => 174
	i32 4015948917, ; 612: Xamarin.AndroidX.Annotation.Jvm.dll => 0xef5e8475 => 211
	i32 4025784931, ; 613: System.Memory => 0xeff49a63 => 62
	i32 4046471985, ; 614: Microsoft.Maui.Controls.Xaml.dll => 0xf1304331 => 190
	i32 4054681211, ; 615: System.Reflection.Emit.ILGeneration => 0xf1ad867b => 90
	i32 4066802364, ; 616: SkiaSharp.HarfBuzz => 0xf2667abc => 196
	i32 4068434129, ; 617: System.Private.Xml.Linq.dll => 0xf27f60d1 => 87
	i32 4073602200, ; 618: System.Threading.dll => 0xf2ce3c98 => 148
	i32 4079385022, ; 619: MySqlConnector.dll => 0xf32679be => 194
	i32 4091086043, ; 620: el\Microsoft.Maui.Controls.resources.dll => 0xf3d904db => 291
	i32 4094352644, ; 621: Microsoft.Maui.Essentials.dll => 0xf40add04 => 192
	i32 4099507663, ; 622: System.Drawing.dll => 0xf45985cf => 36
	i32 4100113165, ; 623: System.Private.Uri => 0xf462c30d => 86
	i32 4101593132, ; 624: Xamarin.AndroidX.Emoji2 => 0xf479582c => 232
	i32 4103439459, ; 625: uk\Microsoft.Maui.Controls.resources.dll => 0xf4958463 => 315
	i32 4126470640, ; 626: Microsoft.Extensions.DependencyInjection => 0xf5f4f1f0 => 181
	i32 4127667938, ; 627: System.IO.FileSystem.Watcher => 0xf60736e2 => 50
	i32 4130442656, ; 628: System.AppContext => 0xf6318da0 => 6
	i32 4147896353, ; 629: System.Reflection.Emit.ILGeneration.dll => 0xf73be021 => 90
	i32 4150914736, ; 630: uk\Microsoft.Maui.Controls.resources => 0xf769eeb0 => 315
	i32 4151237749, ; 631: System.Core => 0xf76edc75 => 21
	i32 4159265925, ; 632: System.Xml.XmlSerializer => 0xf7e95c85 => 162
	i32 4161255271, ; 633: System.Reflection.TypeExtensions => 0xf807b767 => 96
	i32 4164802419, ; 634: System.IO.FileSystem.Watcher.dll => 0xf83dd773 => 50
	i32 4181436372, ; 635: System.Runtime.Serialization.Primitives => 0xf93ba7d4 => 113
	i32 4182413190, ; 636: Xamarin.AndroidX.Lifecycle.ViewModelSavedState.dll => 0xf94a8f86 => 248
	i32 4185676441, ; 637: System.Security => 0xf97c5a99 => 130
	i32 4196529839, ; 638: System.Net.WebClient.dll => 0xfa21f6af => 76
	i32 4213026141, ; 639: System.Diagnostics.DiagnosticSource.dll => 0xfb1dad5d => 27
	i32 4249188766, ; 640: nb\Microsoft.Maui.Controls.resources.dll => 0xfd45799e => 304
	i32 4256097574, ; 641: Xamarin.AndroidX.Core.Core.Ktx => 0xfdaee526 => 225
	i32 4258378803, ; 642: Xamarin.AndroidX.Lifecycle.ViewModel.Ktx => 0xfdd1b433 => 247
	i32 4260525087, ; 643: System.Buffers => 0xfdf2741f => 7
	i32 4271975918, ; 644: Microsoft.Maui.Controls.dll => 0xfea12dee => 189
	i32 4274976490, ; 645: System.Runtime.Numerics => 0xfecef6ea => 110
	i32 4292120959, ; 646: Xamarin.AndroidX.Lifecycle.ViewModelSavedState => 0xffd4917f => 248
	i32 4294763496 ; 647: Xamarin.AndroidX.ExifInterface.dll => 0xfffce3e8 => 234
], align 4

@assembly_image_cache_indices = dso_local local_unnamed_addr constant [648 x i32] [
	i32 68, ; 0
	i32 67, ; 1
	i32 177, ; 2
	i32 108, ; 3
	i32 244, ; 4
	i32 278, ; 5
	i32 48, ; 6
	i32 286, ; 7
	i32 80, ; 8
	i32 295, ; 9
	i32 145, ; 10
	i32 30, ; 11
	i32 319, ; 12
	i32 124, ; 13
	i32 193, ; 14
	i32 102, ; 15
	i32 303, ; 16
	i32 262, ; 17
	i32 107, ; 18
	i32 262, ; 19
	i32 139, ; 20
	i32 282, ; 21
	i32 318, ; 22
	i32 311, ; 23
	i32 77, ; 24
	i32 124, ; 25
	i32 13, ; 26
	i32 218, ; 27
	i32 202, ; 28
	i32 132, ; 29
	i32 264, ; 30
	i32 151, ; 31
	i32 18, ; 32
	i32 216, ; 33
	i32 26, ; 34
	i32 238, ; 35
	i32 1, ; 36
	i32 59, ; 37
	i32 42, ; 38
	i32 91, ; 39
	i32 201, ; 40
	i32 221, ; 41
	i32 147, ; 42
	i32 240, ; 43
	i32 237, ; 44
	i32 54, ; 45
	i32 69, ; 46
	i32 316, ; 47
	i32 207, ; 48
	i32 83, ; 49
	i32 294, ; 50
	i32 239, ; 51
	i32 131, ; 52
	i32 55, ; 53
	i32 149, ; 54
	i32 74, ; 55
	i32 145, ; 56
	i32 62, ; 57
	i32 146, ; 58
	i32 323, ; 59
	i32 165, ; 60
	i32 314, ; 61
	i32 222, ; 62
	i32 12, ; 63
	i32 235, ; 64
	i32 125, ; 65
	i32 152, ; 66
	i32 113, ; 67
	i32 166, ; 68
	i32 164, ; 69
	i32 237, ; 70
	i32 250, ; 71
	i32 292, ; 72
	i32 84, ; 73
	i32 187, ; 74
	i32 195, ; 75
	i32 150, ; 76
	i32 282, ; 77
	i32 60, ; 78
	i32 313, ; 79
	i32 183, ; 80
	i32 51, ; 81
	i32 103, ; 82
	i32 114, ; 83
	i32 40, ; 84
	i32 275, ; 85
	i32 273, ; 86
	i32 120, ; 87
	i32 52, ; 88
	i32 44, ; 89
	i32 119, ; 90
	i32 227, ; 91
	i32 305, ; 92
	i32 233, ; 93
	i32 81, ; 94
	i32 321, ; 95
	i32 136, ; 96
	i32 269, ; 97
	i32 214, ; 98
	i32 8, ; 99
	i32 73, ; 100
	i32 155, ; 101
	i32 284, ; 102
	i32 154, ; 103
	i32 92, ; 104
	i32 279, ; 105
	i32 45, ; 106
	i32 283, ; 107
	i32 109, ; 108
	i32 129, ; 109
	i32 176, ; 110
	i32 25, ; 111
	i32 204, ; 112
	i32 72, ; 113
	i32 55, ; 114
	i32 46, ; 115
	i32 311, ; 116
	i32 196, ; 117
	i32 186, ; 118
	i32 228, ; 119
	i32 22, ; 120
	i32 242, ; 121
	i32 86, ; 122
	i32 43, ; 123
	i32 160, ; 124
	i32 71, ; 125
	i32 255, ; 126
	i32 296, ; 127
	i32 3, ; 128
	i32 42, ; 129
	i32 63, ; 130
	i32 310, ; 131
	i32 16, ; 132
	i32 53, ; 133
	i32 307, ; 134
	i32 278, ; 135
	i32 105, ; 136
	i32 283, ; 137
	i32 300, ; 138
	i32 276, ; 139
	i32 239, ; 140
	i32 34, ; 141
	i32 158, ; 142
	i32 85, ; 143
	i32 32, ; 144
	i32 309, ; 145
	i32 12, ; 146
	i32 51, ; 147
	i32 56, ; 148
	i32 259, ; 149
	i32 36, ; 150
	i32 182, ; 151
	i32 277, ; 152
	i32 178, ; 153
	i32 212, ; 154
	i32 35, ; 155
	i32 290, ; 156
	i32 58, ; 157
	i32 246, ; 158
	i32 173, ; 159
	i32 17, ; 160
	i32 280, ; 161
	i32 164, ; 162
	i32 312, ; 163
	i32 306, ; 164
	i32 302, ; 165
	i32 245, ; 166
	i32 185, ; 167
	i32 272, ; 168
	i32 308, ; 169
	i32 153, ; 170
	i32 268, ; 171
	i32 253, ; 172
	i32 214, ; 173
	i32 29, ; 174
	i32 52, ; 175
	i32 273, ; 176
	i32 5, ; 177
	i32 288, ; 178
	i32 263, ; 179
	i32 267, ; 180
	i32 219, ; 181
	i32 284, ; 182
	i32 211, ; 183
	i32 177, ; 184
	i32 230, ; 185
	i32 297, ; 186
	i32 85, ; 187
	i32 272, ; 188
	i32 61, ; 189
	i32 112, ; 190
	i32 317, ; 191
	i32 57, ; 192
	i32 318, ; 193
	i32 259, ; 194
	i32 99, ; 195
	i32 19, ; 196
	i32 223, ; 197
	i32 111, ; 198
	i32 101, ; 199
	i32 102, ; 200
	i32 286, ; 201
	i32 104, ; 202
	i32 276, ; 203
	i32 71, ; 204
	i32 38, ; 205
	i32 32, ; 206
	i32 103, ; 207
	i32 73, ; 208
	i32 292, ; 209
	i32 9, ; 210
	i32 123, ; 211
	i32 46, ; 212
	i32 213, ; 213
	i32 187, ; 214
	i32 9, ; 215
	i32 43, ; 216
	i32 4, ; 217
	i32 260, ; 218
	i32 194, ; 219
	i32 316, ; 220
	i32 31, ; 221
	i32 138, ; 222
	i32 92, ; 223
	i32 93, ; 224
	i32 49, ; 225
	i32 141, ; 226
	i32 322, ; 227
	i32 112, ; 228
	i32 140, ; 229
	i32 229, ; 230
	i32 115, ; 231
	i32 277, ; 232
	i32 157, ; 233
	i32 76, ; 234
	i32 79, ; 235
	i32 249, ; 236
	i32 37, ; 237
	i32 198, ; 238
	i32 271, ; 239
	i32 233, ; 240
	i32 226, ; 241
	i32 64, ; 242
	i32 138, ; 243
	i32 15, ; 244
	i32 116, ; 245
	i32 265, ; 246
	i32 274, ; 247
	i32 221, ; 248
	i32 48, ; 249
	i32 70, ; 250
	i32 80, ; 251
	i32 126, ; 252
	i32 94, ; 253
	i32 121, ; 254
	i32 281, ; 255
	i32 320, ; 256
	i32 26, ; 257
	i32 321, ; 258
	i32 242, ; 259
	i32 97, ; 260
	i32 28, ; 261
	i32 217, ; 262
	i32 287, ; 263
	i32 149, ; 264
	i32 169, ; 265
	i32 4, ; 266
	i32 98, ; 267
	i32 33, ; 268
	i32 93, ; 269
	i32 264, ; 270
	i32 183, ; 271
	i32 21, ; 272
	i32 41, ; 273
	i32 170, ; 274
	i32 303, ; 275
	i32 235, ; 276
	i32 295, ; 277
	i32 249, ; 278
	i32 280, ; 279
	i32 274, ; 280
	i32 254, ; 281
	i32 2, ; 282
	i32 134, ; 283
	i32 111, ; 284
	i32 184, ; 285
	i32 204, ; 286
	i32 312, ; 287
	i32 58, ; 288
	i32 95, ; 289
	i32 294, ; 290
	i32 39, ; 291
	i32 215, ; 292
	i32 25, ; 293
	i32 94, ; 294
	i32 288, ; 295
	i32 89, ; 296
	i32 99, ; 297
	i32 10, ; 298
	i32 87, ; 299
	i32 299, ; 300
	i32 100, ; 301
	i32 261, ; 302
	i32 179, ; 303
	i32 281, ; 304
	i32 206, ; 305
	i32 291, ; 306
	i32 7, ; 307
	i32 246, ; 308
	i32 203, ; 309
	i32 88, ; 310
	i32 241, ; 311
	i32 154, ; 312
	i32 290, ; 313
	i32 33, ; 314
	i32 116, ; 315
	i32 82, ; 316
	i32 20, ; 317
	i32 11, ; 318
	i32 162, ; 319
	i32 3, ; 320
	i32 191, ; 321
	i32 298, ; 322
	i32 186, ; 323
	i32 184, ; 324
	i32 84, ; 325
	i32 285, ; 326
	i32 64, ; 327
	i32 300, ; 328
	i32 268, ; 329
	i32 143, ; 330
	i32 250, ; 331
	i32 157, ; 332
	i32 41, ; 333
	i32 117, ; 334
	i32 180, ; 335
	i32 205, ; 336
	i32 257, ; 337
	i32 131, ; 338
	i32 75, ; 339
	i32 66, ; 340
	i32 304, ; 341
	i32 172, ; 342
	i32 209, ; 343
	i32 143, ; 344
	i32 106, ; 345
	i32 151, ; 346
	i32 70, ; 347
	i32 200, ; 348
	i32 199, ; 349
	i32 298, ; 350
	i32 156, ; 351
	i32 179, ; 352
	i32 121, ; 353
	i32 127, ; 354
	i32 299, ; 355
	i32 152, ; 356
	i32 232, ; 357
	i32 0, ; 358
	i32 141, ; 359
	i32 219, ; 360
	i32 296, ; 361
	i32 20, ; 362
	i32 14, ; 363
	i32 135, ; 364
	i32 75, ; 365
	i32 59, ; 366
	i32 222, ; 367
	i32 167, ; 368
	i32 168, ; 369
	i32 189, ; 370
	i32 15, ; 371
	i32 74, ; 372
	i32 6, ; 373
	i32 23, ; 374
	i32 302, ; 375
	i32 244, ; 376
	i32 203, ; 377
	i32 91, ; 378
	i32 297, ; 379
	i32 178, ; 380
	i32 1, ; 381
	i32 136, ; 382
	i32 301, ; 383
	i32 245, ; 384
	i32 267, ; 385
	i32 134, ; 386
	i32 69, ; 387
	i32 146, ; 388
	i32 306, ; 389
	i32 285, ; 390
	i32 236, ; 391
	i32 185, ; 392
	i32 88, ; 393
	i32 96, ; 394
	i32 226, ; 395
	i32 231, ; 396
	i32 199, ; 397
	i32 301, ; 398
	i32 31, ; 399
	i32 45, ; 400
	i32 240, ; 401
	i32 322, ; 402
	i32 205, ; 403
	i32 109, ; 404
	i32 158, ; 405
	i32 35, ; 406
	i32 22, ; 407
	i32 114, ; 408
	i32 57, ; 409
	i32 265, ; 410
	i32 144, ; 411
	i32 118, ; 412
	i32 120, ; 413
	i32 110, ; 414
	i32 207, ; 415
	i32 139, ; 416
	i32 213, ; 417
	i32 287, ; 418
	i32 54, ; 419
	i32 105, ; 420
	i32 307, ; 421
	i32 190, ; 422
	i32 191, ; 423
	i32 133, ; 424
	i32 279, ; 425
	i32 270, ; 426
	i32 258, ; 427
	i32 313, ; 428
	i32 236, ; 429
	i32 197, ; 430
	i32 193, ; 431
	i32 159, ; 432
	i32 223, ; 433
	i32 163, ; 434
	i32 132, ; 435
	i32 258, ; 436
	i32 161, ; 437
	i32 247, ; 438
	i32 140, ; 439
	i32 270, ; 440
	i32 266, ; 441
	i32 169, ; 442
	i32 192, ; 443
	i32 200, ; 444
	i32 208, ; 445
	i32 275, ; 446
	i32 40, ; 447
	i32 234, ; 448
	i32 81, ; 449
	i32 56, ; 450
	i32 37, ; 451
	i32 97, ; 452
	i32 166, ; 453
	i32 172, ; 454
	i32 197, ; 455
	i32 271, ; 456
	i32 82, ; 457
	i32 210, ; 458
	i32 98, ; 459
	i32 30, ; 460
	i32 159, ; 461
	i32 18, ; 462
	i32 127, ; 463
	i32 119, ; 464
	i32 230, ; 465
	i32 261, ; 466
	i32 243, ; 467
	i32 263, ; 468
	i32 165, ; 469
	i32 238, ; 470
	i32 323, ; 471
	i32 293, ; 472
	i32 260, ; 473
	i32 251, ; 474
	i32 170, ; 475
	i32 16, ; 476
	i32 144, ; 477
	i32 175, ; 478
	i32 125, ; 479
	i32 118, ; 480
	i32 38, ; 481
	i32 115, ; 482
	i32 47, ; 483
	i32 142, ; 484
	i32 117, ; 485
	i32 34, ; 486
	i32 202, ; 487
	i32 173, ; 488
	i32 95, ; 489
	i32 53, ; 490
	i32 252, ; 491
	i32 129, ; 492
	i32 153, ; 493
	i32 24, ; 494
	i32 161, ; 495
	i32 229, ; 496
	i32 148, ; 497
	i32 104, ; 498
	i32 201, ; 499
	i32 89, ; 500
	i32 217, ; 501
	i32 60, ; 502
	i32 142, ; 503
	i32 100, ; 504
	i32 5, ; 505
	i32 13, ; 506
	i32 122, ; 507
	i32 135, ; 508
	i32 28, ; 509
	i32 293, ; 510
	i32 72, ; 511
	i32 227, ; 512
	i32 24, ; 513
	i32 195, ; 514
	i32 215, ; 515
	i32 256, ; 516
	i32 253, ; 517
	i32 310, ; 518
	i32 137, ; 519
	i32 208, ; 520
	i32 224, ; 521
	i32 168, ; 522
	i32 257, ; 523
	i32 289, ; 524
	i32 175, ; 525
	i32 101, ; 526
	i32 123, ; 527
	i32 228, ; 528
	i32 181, ; 529
	i32 163, ; 530
	i32 167, ; 531
	i32 231, ; 532
	i32 39, ; 533
	i32 188, ; 534
	i32 308, ; 535
	i32 17, ; 536
	i32 198, ; 537
	i32 171, ; 538
	i32 309, ; 539
	i32 137, ; 540
	i32 150, ; 541
	i32 220, ; 542
	i32 0, ; 543
	i32 320, ; 544
	i32 155, ; 545
	i32 130, ; 546
	i32 19, ; 547
	i32 65, ; 548
	i32 176, ; 549
	i32 147, ; 550
	i32 47, ; 551
	i32 317, ; 552
	i32 319, ; 553
	i32 206, ; 554
	i32 79, ; 555
	i32 61, ; 556
	i32 106, ; 557
	i32 255, ; 558
	i32 210, ; 559
	i32 49, ; 560
	i32 241, ; 561
	i32 314, ; 562
	i32 252, ; 563
	i32 14, ; 564
	i32 180, ; 565
	i32 68, ; 566
	i32 171, ; 567
	i32 216, ; 568
	i32 220, ; 569
	i32 78, ; 570
	i32 225, ; 571
	i32 108, ; 572
	i32 209, ; 573
	i32 251, ; 574
	i32 67, ; 575
	i32 63, ; 576
	i32 27, ; 577
	i32 160, ; 578
	i32 289, ; 579
	i32 218, ; 580
	i32 10, ; 581
	i32 174, ; 582
	i32 188, ; 583
	i32 11, ; 584
	i32 78, ; 585
	i32 126, ; 586
	i32 83, ; 587
	i32 182, ; 588
	i32 66, ; 589
	i32 107, ; 590
	i32 65, ; 591
	i32 128, ; 592
	i32 122, ; 593
	i32 77, ; 594
	i32 266, ; 595
	i32 256, ; 596
	i32 8, ; 597
	i32 224, ; 598
	i32 2, ; 599
	i32 305, ; 600
	i32 44, ; 601
	i32 269, ; 602
	i32 156, ; 603
	i32 128, ; 604
	i32 254, ; 605
	i32 23, ; 606
	i32 133, ; 607
	i32 212, ; 608
	i32 243, ; 609
	i32 29, ; 610
	i32 174, ; 611
	i32 211, ; 612
	i32 62, ; 613
	i32 190, ; 614
	i32 90, ; 615
	i32 196, ; 616
	i32 87, ; 617
	i32 148, ; 618
	i32 194, ; 619
	i32 291, ; 620
	i32 192, ; 621
	i32 36, ; 622
	i32 86, ; 623
	i32 232, ; 624
	i32 315, ; 625
	i32 181, ; 626
	i32 50, ; 627
	i32 6, ; 628
	i32 90, ; 629
	i32 315, ; 630
	i32 21, ; 631
	i32 162, ; 632
	i32 96, ; 633
	i32 50, ; 634
	i32 113, ; 635
	i32 248, ; 636
	i32 130, ; 637
	i32 76, ; 638
	i32 27, ; 639
	i32 304, ; 640
	i32 225, ; 641
	i32 247, ; 642
	i32 7, ; 643
	i32 189, ; 644
	i32 110, ; 645
	i32 248, ; 646
	i32 234 ; 647
], align 4

@marshal_methods_number_of_classes = dso_local local_unnamed_addr constant i32 0, align 4

@marshal_methods_class_cache = dso_local local_unnamed_addr global [0 x %struct.MarshalMethodsManagedClass] zeroinitializer, align 4

; Names of classes in which marshal methods reside
@mm_class_names = dso_local local_unnamed_addr constant [0 x ptr] zeroinitializer, align 4

@mm_method_names = dso_local local_unnamed_addr constant [1 x %struct.MarshalMethodName] [
	%struct.MarshalMethodName {
		i64 0, ; id 0x0; name: 
		ptr @.MarshalMethodName.0_name; char* name
	} ; 0
], align 8

; get_function_pointer (uint32_t mono_image_index, uint32_t class_index, uint32_t method_token, void*& target_ptr)
@get_function_pointer = internal dso_local unnamed_addr global ptr null, align 4

; Functions

; Function attributes: "min-legal-vector-width"="0" mustprogress nofree norecurse nosync "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8" uwtable willreturn
define void @xamarin_app_init(ptr nocapture noundef readnone %env, ptr noundef %fn) local_unnamed_addr #0
{
	%fnIsNull = icmp eq ptr %fn, null
	br i1 %fnIsNull, label %1, label %2

1: ; preds = %0
	%putsResult = call noundef i32 @puts(ptr @.str.0)
	call void @abort()
	unreachable 

2: ; preds = %1, %0
	store ptr %fn, ptr @get_function_pointer, align 4, !tbaa !3
	ret void
}

; Strings
@.str.0 = private unnamed_addr constant [40 x i8] c"get_function_pointer MUST be specified\0A\00", align 1

;MarshalMethodName
@.MarshalMethodName.0_name = private unnamed_addr constant [1 x i8] c"\00", align 1

; External functions

; Function attributes: noreturn "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8"
declare void @abort() local_unnamed_addr #2

; Function attributes: nofree nounwind
declare noundef i32 @puts(ptr noundef) local_unnamed_addr #1
attributes #0 = { "min-legal-vector-width"="0" mustprogress nofree norecurse nosync "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8" "stackrealign" "target-cpu"="i686" "target-features"="+cx8,+mmx,+sse,+sse2,+sse3,+ssse3,+x87" "tune-cpu"="generic" uwtable willreturn }
attributes #1 = { nofree nounwind }
attributes #2 = { noreturn "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8" "stackrealign" "target-cpu"="i686" "target-features"="+cx8,+mmx,+sse,+sse2,+sse3,+ssse3,+x87" "tune-cpu"="generic" }

; Metadata
!llvm.module.flags = !{!0, !1, !7}
!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!llvm.ident = !{!2}
!2 = !{!"Xamarin.Android remotes/origin/release/8.0.1xx @ af27162bee43b7fecdca59b4f67aa8c175cbc875"}
!3 = !{!4, !4, i64 0}
!4 = !{!"any pointer", !5, i64 0}
!5 = !{!"omnipotent char", !6, i64 0}
!6 = !{!"Simple C++ TBAA"}
!7 = !{i32 1, !"NumRegisterParameters", i32 0}
