<template>
    <Header />
    <QuestionMenu />
     <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif">
        </div>
        <div v-bind:class="[ContentClass]">
            <h3 class="table-name" style="color: #00415d;">
                Редактирование вопроса
             </h3><br>
            <QuestionGrid>
                 <template v-slot:q-level>
                    <div class="half-block">
                        Выберите из списка: <select class="form-control text-center" v-model="questionLevel">
                            <option value="" disabled selected hidden>Выберите Тема</option>
                            <option v-for="level in listLevels">
                                {{ level.level }}
                            </option>
                        </select>
                    </div>
                 </template>
                 <template v-slot:q-type>
                    <div class="half-block">
                        Выберите из списка: <select class="form-control text-center" v-model="questionType">
                            <option v-for="type in listTypes">
                                {{ type }}
                            </option>
                        </select>
                    </div>
                 </template>
                 <template v-slot:q-text>
                    <div style="padding-bottom: 15px;">
                        <editor
                           v-model="question_mce"
                           api-key="p0t8lf7pix6acnxfbd8i3ako0vo4ke98tll8pe4mufqr1hcw"
                           :init="{
                             height: 500,
                             menubar: 'edit table',
                             language: 'ru',
                             plugins: [
                               'advlist autolink lists link image charmap print preview anchor',
                               'searchreplace visualblocks code fullscreen',
                               'insertdatetime media table paste code help wordcount'
                             ],
                             toolbar:
                               'undo redo | bold italic underline strikethrough | \
                               fontselect fontsizeselect formatselect | \
                               alignleft aligncenter alignright alignjustify | \
                               outdent indent |  numlist bullist checklist | \
                               forecolor backcolor casechange permanentpen formatpainter removeformat | \
                               pagebreak | charmap emoticons | fullscreen  preview save | \
                               insertfile image pageembed template link codesample | \
                               a11ycheck ltr rtl',
                             images_upload_handler: (blobInfo, success, failure) => {
                                imagesUploadHandler(blobInfo, success, failure)
                             }
                           }"
                         />
                    </div>
                 </template>
            </QuestionGrid><br>
            <div v-bind:class="[ButtonLoadClass]">
                <img src="../../../assets/gifs/load.gif" style="margin: 0 auto;">
            </div>
            <div v-bind:class="[ButtonClass]">
                <button class="btn btn-lg btn-primary m-auto iohk-butt"
                    type="button" @click="saveQuestion();">
                    Сохранить изменения
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    import Header from "../../../components/Header.vue"
    import SideBox from "../../../components/SideBox.vue"
    import QuestionMenu from "../../../components/QuestionMenu.vue"
    import QuestionGrid from "../../../components/QuestionGrid.vue"
    import Editor from '@tinymce/tinymce-vue'

    export default {
        name: "EditQuestion",
        components: {
            Header,
            QuestionMenu,
            SideBox,
            QuestionGrid,
            'editor': Editor
        },
        data() {
            return {
                currentQuestion: '',
                listLevels: [],
                currentType: '',
                listTypes: ['Классический', 'Соответствие', 'Краткий ответ', 'Табличный', 'Развернутый ответ'],
                ButtonClass: 'vue-active',
                ButtonLoadClass: 'vue-deactive',
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
            }
        },
        methods: {
            async getLevels() {
                let url = ''
                if (this.findString != ''){
                    url = this.$store.state.backendUrl+'/api/service/levels?ordering='+this.sort+'&'+this.findString
                } else {
                    url = this.$store.state.backendUrl+'/api/service/levels?ordering='+this.sort
                }
                this.listLevels = await fetch(url, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json()
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
            async imagesUploadHandler(blobInfo, success, failure) {
                var formRequest = new FormData();
                formRequest.append('file', blobInfo.blob(), blobInfo.filename());
                await fetch (this.$store.state.backendUrl+'/api/service/upload_image/', {
                    method: 'PUT',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                    },
                    body: formRequest
                })
                .then(resp => resp.json())
                .then(data => {
                    if (data.location) {
                        success(this.$store.state.backendUrl+data.location)
                    } else {
                        failure(data.error)
                    }
                })
            },
            async addQuestion() {
                this.ButtonClass = 'vue-deactive'
                this.ButtonLoadClass = 'vue-active'
                if (this.questionLevel == null) {
                    showBanner('.banner.error', 'Выберите Тема вопроса')
                    this.ButtonClass = 'vue-active'
                    this.ButtonLoadClass = 'vue-deactive'
                } else if (this.questionType == null) {
                    showBanner('.banner.error', 'Выберите тип вопроса')
                    this.ButtonClass = 'vue-active'
                    this.ButtonLoadClass = 'vue-deactive'
                } else if (this.question_mce == null) {
                    showBanner('.banner.error', 'Заполните формулировку вопроса')
                    this.ButtonClass = 'vue-active'
                    this.ButtonLoadClass = 'vue-deactive'
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/question_new/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'level': this.questionLevel,
                        'type': this.questionType,
                        'question': this.question_mce,
                      })
                    })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data.error) {
                           showBanner('.banner.error', data.error)
                           this.ButtonClass = 'vue-active'
                           this.ButtonLoadClass = 'vue-deactive'
                           return false
                        } else {
                           this.$router.push('/admin/answers?question_id='+data.success)
                        }
                    })
                }
            },
            async getQuestion() {
                this.currentQuestion = await fetch(this.$store.state.backendUrl+'/api/service/question/'+this.$route.query.question_id+'/', {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json()
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка при получении вопроса, повторите попытку позже')
                     return false
                  }
                })
                this.getLevels()
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
                this.questionLevel = this.currentQuestion.level
                this.questionType = this.currentQuestion.type
                this.question_mce = this.currentQuestion.question
            },
            async saveQuestion() {
                this.ButtonClass = 'vue-deactive'
                this.ButtonLoadClass = 'vue-active'
                if (this.questionLevel == null) {
                    showBanner('.banner.error', 'Выберите Тема вопроса')
                    this.ButtonClass = 'vue-active'
                    this.ButtonLoadClass = 'vue-deactive'
                } else if (this.questionType == null) {
                    showBanner('.banner.error', 'Выберите тип вопроса')
                    this.ButtonClass = 'vue-active'
                    this.ButtonLoadClass = 'vue-deactive'
                } else if (this.question_mce == null) {
                    showBanner('.banner.error', 'Заполните формулировку вопроса')
                    this.ButtonClass = 'vue-active'
                    this.ButtonLoadClass = 'vue-deactive'
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/question_update/'+this.$route.query.question_id+'/', {
                      method: 'PUT',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'level': this.questionLevel,
                        'type': this.questionType,
                        'question': this.question_mce,
                      })
                    })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data.error) {
                           showBanner('.banner.error', data.error)
                           this.ButtonClass = 'vue-active'
                           this.ButtonLoadClass = 'vue-deactive'
                           return false
                        } else {
                           showBanner('.banner.success', data.success);
                           this.$router.push('/admin/questions')
                        }
                    })
                }
            }
        },
        created() {
            this.getQuestion()
        }
    }
</script>

<style>
.half-block{
    margin: 0 auto;
    width: 50%;
    margin-bottom: 5px;
}
</style>