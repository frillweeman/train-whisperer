<script lang="ts">
  import VirtualList from "$lib/global-components/VirtualList.svelte";
  import { getModalStore } from "@skeletonlabs/skeleton";
  import type { ModalSettings } from '@skeletonlabs/skeleton';
  import { createEventDispatcher } from "svelte";

  export let messages = [];
  export let channelNames = [""];

  const modalStore = getModalStore();
  const dispatch = createEventDispatcher();
  
  function showModal(channelNumber: number) {
    const modal: ModalSettings = {
      type: 'prompt',
      title: 'Rename Channel',
      body: `Please enter a new name for channel ${channelNumber}.`,
      valueAttr: { type: 'text', minlength: 2, maxlength: 10, required: true },
      
      // Returns the updated response value
      response: (newChannelName: string) => {
        dispatch('renameChannel', { channelNumber, newChannelName });
      },
    };
    modalStore.trigger(modal);
  }

</script>

<div class="chat-container overflow-auto pt-3 px-4">
  <VirtualList items={messages} let:item autoScroll>
    <div
      class="chat chat-start my-2"
      class:text-left={item.channelIndex === 1}
      class:text-right={item.channelIndex === 2}
    >
      <div class="chat-bubble mb-0">{item.text}</div>
      <div class="chat-footer mt-0">
        <span on:click={showModal.bind(null, item.channelIndex)} class="text-xs font-bold cursor-pointer">{channelNames[item.channelIndex - 1] ?? "Broadcast"}</span>
        <time class="text-xs opacity-50">{new Date(item.timestamp).toLocaleTimeString([], {
          timeStyle: "short",
        })}</time>
      </div>
    </div>
  </VirtualList>
</div>

<style>
.chat-container {
  height: calc(100vh - 208px);
}
</style>
