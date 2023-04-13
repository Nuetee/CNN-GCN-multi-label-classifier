<template>
  <div class="home">
    <input type="file" accept="image/jpg, image/jpeg" id="imageUpload">
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
    }
  },
  async mounted () {
    this.sess = new onnx.InferenceSession()
    await this.sess.loadModel(process.env.BASE_URL + 'resnet50_model.onnx')

    this.imageUpload = document.getElementById('imageUpload')
            
    this.$nextTick(() => {
        this.imageUpload.addEventListener('change', this.changeImage)
    })
  },
  methods: {
    async changeImage () {
      let imgData = this.imageUpload.files[0]
      const reader = new FileReader()

      reader.onload = async () => {
        const arrayBuffer = reader.result
        const img = new Image()
        img.onload = async () => {
          const canvas = document.createElement("canvas")
          canvas.width = 224
          canvas.height = 224
          const ctx = canvas.getContext("2d")
          ctx.drawImage(img, 0, 0, 224, 224)
          const imgData = ctx.getImageData(0, 0, 224, 224)
          const inputArray = new Float32Array(imgData.data)
          const inputShape = [1, 3, 224, 224];
          // Alpha 채널 제거
          const inputArrayReshaped = new Float32Array(3 * 224 * 224);
          for (let i = 0; i < 224 * 224; i++) {
            for (let j = 0; j < 3; j++) {
              inputArrayReshaped[i * 3 + j] = inputArray[i * 4 + j];
            }
          }
          if (inputArrayReshaped.length !== inputShape.reduce((a, b) => a * b)) {
            throw new Error("Input dims doesn't match data length.");
          }
          const input = new onnx.Tensor(inputArrayReshaped, "float32", inputShape)
          const outputMap = await this.sess.run([input])
          const outputTensor = outputMap.values().next().value
          const predictions = outputTensor.data
          console.log(predictions)
        };
        img.src = URL.createObjectURL(new Blob([arrayBuffer]));
      };
      reader.readAsArrayBuffer(imgData)
    }
  }
}
</script>
