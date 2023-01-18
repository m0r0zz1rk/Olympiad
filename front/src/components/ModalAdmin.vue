<template>
    <transition name="modal-fade">
        <div class="modal-overlay">
            <div class="modal">
                  <slot name="main-info"></slot>
            </div>
            <div class="close" @click="$emit('close-modal')">
                <img class="close-img" src="../assets/img/modal/close-icon.png" alt="" />
            </div>
        </div>
    </transition>
</template>

<script>
    export default {
        name: "ModalAdmin"
    }
</script>

<style scoped>
    .modal-overlay {
      position: fixed;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
      display: flex;
      justify-content: center;
      background-color: #000000da;
    }

    .modal {
      display: block;
      position: relative;
      text-align: center;
      background-color: white;
      height: 90vh;
      width: 90vw;
      border-radius: 20px;
    }

    .contain{
      width: 80%;
      height: 80%;
      top: 0;
      left: 0;
      bottom: 0;
      right: 0;
      margin: auto;
      position: absolute;
    }

    .close {
      margin: 10% 0 0 16px;
      cursor: pointer;
    }

    .close-img {
      width: 25px;
    }

    .check {
      width: 150px;
    }

    h6 {
      font-weight: 500;
      font-size: 28px;
      margin: 20px 0;
    }

    p {
      font-size: 16px;
      margin: 20px 0;
    }

    button {
      background-color: #ac003e;
      width: 150px;
      height: 40px;
      color: white;
      font-size: 14px;
      border-radius: 16px;
      margin-top: 50px;
    }
    .modal-fade-enter,
    .modal-fade-leave-to {
      opacity: 0;
    }
    .modal-fade-enter-active,
    .modal-fade-leave-active {
      transition: opacity 0.5s ease;
    }
</style>