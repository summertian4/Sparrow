<template>
  <div>
    <div class="sparrow-content">
      <h1 class="title">返回模板选择器</h1>
      <div class="block is-flex">
        <tabs animation="slide" :only-fade="false">
          <tab-pane label="公共模板">
            <div class="search">
              <input type="text" placeholder="请输入关键字...">
              <div class="block is-flex">
                <collapse>
                  <collapse-item title="Components">
                    <form @submit.prevent="submit">
                      <label class="label">模板名称</label>
                      <p class="control has-icon has-icon-right">
                        {{ template.name }}
                      </p>
                      <label class="label">MIME 类型</label>
                      <div class="control">
                        <div v-if="template.mimeType === 0">
                          application/json
                        </div>
                        <div v-if="template.mimeType === 1">
                          text/plain
                        </div>
                        <div v-if="template.mimeType === 2">
                          image/jpeg
                        </div>
                      </div>
                      <label class="label">备注</label>
                      <p class="control">
                        <textarea class="textarea" v-model="template.note" disabled></textarea>
                      </p>
                      <label class="label">数据内容</label>
                      <p class="control">
                        <json-editor ref="editor" :json="template.responseJson"/>
                      </p>
                    </form>
                    <div class="block">
                      <span class="demonstration">大于 7 页时的效果</span>
                      <el-pagination
                        layout="prev, pager, next"
                        :total="1000">
                      </el-pagination>
                    </div>
                  </collapse-item>
                  <collapse-item title="Elements">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus nec iaculis mauris. @bulmaio. #css #responsive
                  </collapse-item>
                </collapse>
              </div>
              <div class="block">
                <el-pagination
                  layout="prev, pager, next"
                  :total="50">
                </el-pagination>
              </div>
            </div>
          </tab-pane>
          <tab-pane label="项目内模板">Pictures Tab</tab-pane>
        </tabs>
      </div>
    </div>
  </div>
</template>

<script>
  import JsonEditor from '../components/JsonEditor'
  import {Tabs, TabPane} from 'vue-bulma-tabs'
  import {Collapse, Item as CollapseItem} from 'vue-bulma-collapse'
  import ElPagination from 'element-pagination'
  import 'element-theme-chalk'

  export default {
    components: {
      JsonEditor,
      Tabs,
      TabPane,
      Collapse,
      CollapseItem,
      ElPagination
    },

    data () {
      return {
        template: {
          name: '233',
          mimeType: 0,
          note: '233',
          responseJson: {}
        }
      }
    },

    created () {
    },

    computed: {},

    methods: {}
  }
</script>

<style scoped>

  .sparrow-content {
    margin: 20px;
  }

  .search input {
    outline: none;
    width: 100%;
    height: 42px;
    padding-left: 13px;
    background-color: #FFFFFF;
    border-radius: 5px;
    border: 1px solid #DDDDDD;
  }

  .search input:focus {
    color: #555555;
    border: 1px solid #5aceb3;
  }

  .box {
    border: 0px;
  }

</style>
