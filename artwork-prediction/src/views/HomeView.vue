<template>
  <div class="home">
    <input type="file" accept="image/jpg, image/jpeg" id="imageUpload">
		<div style="height:300px; display: flex; align-items: center; justify-content: center;">
			<div style="height:256px; width: 256px; background-color: lightgrey;">
				<img :src="this.selectedImage" style="width: 100%; height: 100%">
			</div>
		</div>
		 <div v-if="this.loading" style="display:flex; align-items: center; justify-content: center;">
			loading...
		</div>
		<div v-if="!loading">
			{{ this.predicted_labels }}
		</div>
  </div>
</template>

<script>
// @ is an alias to /src
import * as onnx from 'onnxjs'
export default {
  name: 'HomeView',
  data () {
    return {
      imageUpload: null,
      sess: null,
      selectedImage: null,
      loading: false,
			total_labels: ['photorealism', 'wash', 'sculpture', 'symbolism', 'pointillism', 'woodblock print', 'neoplasticism', 'surrealism', 'fresco', 'p&d (pattern and decoration)', 'japonism', 'feminist art', 'mixed technique', 'hellenistic', 'figurative expressionism', 'abstract expressionism', 'verism', 'sumi-e (suiboku-ga)', 'new european painting', 'tronie', 'contemporary', 'regionalism', 'pop art', 'cloisonnism', 'religious painting ', 'animal painting', 'abstract', 'new realism', 'allegorical painting', 'collage', 'academicism', 'ink and wash painting', 'op art', 'battle painting', 'tenebrism', 'cloudscape', 'orientalism', 'art informel', 'muralism', 'flower painting', 'capriccio', 'photography', 'landscape', 'design ', 'expressionism', 'stone', 'international gothic', 'neo-rococo', 'post-minimalism', 'sōsaku hanga', 'tachisme', 'mannerism (late renaissance)', 'indian ink', 'nouveau réalisme', 'figurative ', 'pastorale', 'neo-figurative art', 'magna', 'crayon', 'hard edge painting', 'graffiti', 'cubism', 'design', 'mythological painting ', 'illustration ', 'yakusha-e', 'masonite', 'pictorialism', 'history painting', 'color field painting', 'graphite', 'paint', 'digital art', 'lyrical abstraction', 'neo-minimalism', 'literary painting', 'utensil', 'impressionism', 'light and space', 'canvas', 'engraving', 'analytical cubism', 'linocut', 'orphism', 'cubo-futurism', 'gouache', 'ukiyo-e', 'interior', 'sculpture ', 'naturalism', 'veduta', 'concretism', 'cardboard', 'pen', 'suprematism', 'pastel', 'religious painting', 'post-impressionism', 'contemporary realism', 'proto renaissance', 'symbiotic art', 'nude painting (nu)', 'watercolor', 'kinetic art', 'tessellation', 'acrylic', 'marina ', 'fabric', 'panel', 'drawing', 'bird-and-flower painting', 'environmental (land) art', 'abstract ', 'chalk', 'silkscreen', 'minimalism', 'miniature', 'mosaïque', 'performance', 'rococo', 'sketch and study ', 'wood', 'neoclassicism', 'neo-expressionism', 'byzantine', 'paper', 'ink', 'charcoal', 'magic realism', 'abstract art', 'luminism', 'street photography', 'print', 'woodcut', 'bronze', 'photomontage', 'aquatint', 'naïve art (primitivism)', 'poster', 'neo-dada', 'oil', 'tempera', 'nude painting (nu) ', 'sketch and study', 'tonalism', 'oak', 'precisionism', 'post-painterly abstraction', 'action painting', 'classicism', 'art brut', 'biedermeier', 'street art', 'modernismo', 'still life', 'installation', 'neo-impressionism', 'art deco', 'safavid period', 'self-portrait', 'digital', 'pencil', 'futurism', 'socialist realism', 'caricature', 'history painting ', 'synthetic cubism', 'advertisement', 'cityscape ', 'conceptual art', 'neo-geo', 'hyper-realism', 'outsider art', 'new kingdom', 'portrait ', 'neo-baroque', 'american realism', 'wall', 'classical realism', 'illustration', 'etching', 'social realism', 'oilcloth', 'symbolic painting ', 'transavantgarde', 'purism', 'brush', 'zen', 'divisionism', 'fantastic realism', 'dada', 'fantasy art', 'photo', 'marina', 'art nouveau (modern)', 'early renaissance', 'high renaissance', 'kitsch', 'architecture', 'metaphysical art', 'baroque', 'realism', 'lithography', 'cityscape', 'mythological painting', 'neo-pop art', 'intimism', 'genre painting', 'northern renaissance', 'genre painting ', 'wildlife painting', 'spatialism', 'shin-hanga', 'portrait', 'costumbrismo', 'calligraphy', 'constructivism', 'neo-romanticism', 'landscape ', 'symbolic painting', 'linen', 'board', 'animal painting ', 'romanticism', 'figurative', 'middle byzantine (c 850–1204)', 'fauvism', 'mixed media', 'postcolonial art'],
			predicted_labels: []
    }
  },
  async mounted () {
    this.sess = new onnx.InferenceSession()
    await this.sess.loadModel(process.env.BASE_URL + 'cnngnn_3_1_5_1_gsc_elu_false_2_0.onnx')

    // this.imageUpload = document.getElementById('imageUpload')

    // this.$nextTick(() => {
    //   this.imageUpload.addEventListener('change', this.changeImage)
    // })
  },
  methods: {
		// sigmoid(z) {
		// 	const k = 2;
		// 	return 1 / (1 + Math.exp(-z/k));
		// },
    // async changeImage () {
    //   const imgData = this.imageUpload.files[0]
    //   this.selectedImage = URL.createObjectURL(imgData)
    //   const reader = new FileReader()

		// 	this.loading = true
    //   reader.onload = async () => {
    //     const arrayBuffer = reader.result
    //     const img = new Image()
    //     img.onload = async () => {
    //       const canvas = document.createElement('canvas')
    //       canvas.width = 224
    //       canvas.height = 224
    //       const ctx = canvas.getContext('2d')
    //       ctx.drawImage(img, 0, 0, 224, 224)
    //       const imgData = ctx.getImageData(0, 0, 224, 224)
    //       const inputArray = new Float32Array(imgData.data)
    //       const inputShape = [1, 3, 224, 224]
    //       // Alpha 채널 제거
    //       const inputArrayReshaped = new Float32Array(3 * 224 * 224)
    //       for (let i = 0; i < 224 * 224; i++) {
    //         for (let j = 0; j < 3; j++) {
    //           inputArrayReshaped[i * 3 + j] = inputArray[i * 4 + j]
    //         }
    //       }
    //       if (inputArrayReshaped.length !== inputShape.reduce((a, b) => a * b)) {
    //         throw new Error("Input dims doesn't match data length.")
    //       }
    //       const input = new onnx.Tensor(inputArrayReshaped, 'float32', inputShape)
    //       const outputMap = await this.sess.run([input])
    //       const outputTensor = outputMap.values().next().value
    //       const predictions = outputTensor.data
		// 			console.log(predictions)
    //       // this.predictLabels(predictions)
		// 			this.loading = false
    //     }
    //     img.src = URL.createObjectURL(new Blob([arrayBuffer]))
    //   }
    //   reader.readAsArrayBuffer(imgData)
    // },
		// predictLabels(predictions) {
		// 	this.predicted_labels = []
		// 	for (let i = 0; i < predictions.length(); i++) {
		// 		if (predictions[i] > 0) {
		// 			this.predicted_labels.push(this.total_labels[i])
		// 		}
		// 	}
		// }
  }
}
</script>
