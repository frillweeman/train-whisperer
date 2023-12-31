<script lang="ts">
  import VirtualList from "$lib/global-components/VirtualList.svelte";
  import { getModalStore } from "@skeletonlabs/skeleton";
  import type { ModalSettings } from '@skeletonlabs/skeleton';
  import { createEventDispatcher } from "svelte";

  export let messages = [];
  export let channelNames = [""];

  let lastItemDisplayed = Number.MAX_SAFE_INTEGER;
  let vList;

  $: areNewItems = messages.length > lastItemDisplayed + 1;

  const modalStore = getModalStore();
  const dispatch = createEventDispatcher();
  const today = new Date();

  function isToday(date: Date) {
    return date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear();
  }
  
  function showModal(channelNumber: number) {
    const modal: ModalSettings = {
      type: 'prompt',
      title: 'Rename Channel',
      body: `Please enter a new name for channel ${channelNumber}.`,
      valueAttr: { type: 'text', minlength: 2, maxlength: 10, required: true },
      
      // Returns the updated response value
      response: (newChannelName: string) => {
        if (!newChannelName)
          return;
        dispatch('renameChannel', { channelNumber, newChannelName });
      },
    };
    modalStore.trigger(modal);
  }

</script>

<div class="chat-container overflow-auto pt-3 px-4 relative">
  {#if areNewItems}
    <div class="absolute bottom-4 z-50 w-full text-center">
      <button on:click={vList.scrollToBottom} class="btn variant-filled-primary">
        <i class="fas fa-arrow-down mr-2" />
        New Messages
      </button>
    </div>
  {/if}
  <VirtualList bind:this={vList} bind:end={lastItemDisplayed} items={messages} let:item autoScroll>
    <div
      class="chat chat-start my-2"
      class:text-left={item.channelIndex === 1}
      class:text-right={item.channelIndex === 2}
    >
      <div class="chat-bubble mb-0">{item.text}</div>
      <div class="chat-footer mt-0">
        <button on:click={showModal.bind(null, item.channelIndex)} class="text-xs font-bold cursor-pointer">{channelNames[item.channelIndex - 1] ?? "Broadcast"}</button>
        <div class="text-xs opacity-50">
          {isToday(new Date(item.timestamp)) ? "" : new Date(item.timestamp).toLocaleDateString([], { month: "numeric", day: "numeric" })}
          <time>{new Date(item.timestamp).toLocaleTimeString([], { timeStyle: "short" })}</time>
        </div>
      </div>
    </div>
  </VirtualList>
</div>

<style>
.chat-container {
  height: calc(100vh - 208px);
}
</style>
