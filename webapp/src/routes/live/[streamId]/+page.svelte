<script lang="ts">
  import Button from "$lib/global-components/Button.svelte";
  import ChatView from "./ChatView.svelte";
  import { popup } from "@skeletonlabs/skeleton";
  import type { PopupSettings } from "@skeletonlabs/skeleton";

  export let data;


  const popupConfirmMonitoring: PopupSettings = {
    event: 'click',
    target: 'confirmMonitoring',
    placement: 'bottom',
  };
            

  enum Status {
    Monitoring = "monitoring",
    Waiting = "waiting",
    Stopped = "stopped"
  };

  let isMuted = false;
  let monitoringStatus = Status.Stopped;

  $: activeStream = data.streams.find(stream => stream.active);

  function toggleAudioStream(): void {
    isMuted = !isMuted;
    // TODO: play/pause audio stream
  }

  function toggleMonitoring(): void {
    switch (monitoringStatus) {
      case Status.Monitoring:
        monitoringStatus = Status.Stopped;
        break;
      case Status.Stopped:
        monitoringStatus = Status.Monitoring;
        break;
      case Status.Waiting:
        monitoringStatus = Status.Monitoring;
        break;
    }
  }
</script>

<div>
  {#if activeStream}
    <div>

      <div class="p-2 sticky left-0 top-0 w-full flex justify-between bg-surface-700 z-10">
        <button use:popup={popupConfirmMonitoring} class="btn-icon hover:variant-soft-primary">
          {#if monitoringStatus === Status.Monitoring}
            <i class="fas fa-circle text-green-500 text-lg" />
          {:else if monitoringStatus === Status.Stopped}
            <i class="fas fa-circle text-red-500 text-lg" />
          {:else if monitoringStatus === Status.Waiting}
            <i class="fas fa-circle text-yellow-500 text-lg" />
          {/if}
        </button>

        <!-- Confirm Popup -->
        <div class="card p-4 w-72 shadow-xl variant-filled-surface" data-popup="confirmMonitoring">
          <div>
            {#if monitoringStatus === Status.Monitoring}
              <p>Are you sure you want to stop monitoring?</p>
              <button class="mt-3 btn w-full variant-filled"><i class="fas fa-stop mr-2" />STOP</button>
              {:else if monitoringStatus === Status.Stopped}
              <p>Are you sure you want to start monitoring? This feature makes use of OpenAI's Whisper API, which can be expensive if run for long periods.</p>
              <button class="mt-3 btn w-full variant-filled"><i class="fas fa-play mr-2" />START</button>
            {:else if monitoringStatus === Status.Waiting}
              <p>Please wait...</p>
            {/if}
          </div>
          <div class="arrow variant-filled-surface" />
        </div>
                  

        <div class="flex items-center max-w-sm truncate">
          <span class="h4 font-bold">{activeStream.title}</span>
        </div>
        
        <button on:click={toggleAudioStream} class="btn-icon hover:variant-soft-primary">
          {#if isMuted}
            <i class="fas fa-volume-mute text-lg" />
          {:else}
            <i class="fas fa-volume-high text-lg" />
          {/if}
        </button>
      </div>

      <ChatView messages={data.transcriptions[`${activeStream.id}`]} channelNames={activeStream.channelNames} />
    </div>
  {:else}
    <div>No active streams</div>
  {/if}
</div>
