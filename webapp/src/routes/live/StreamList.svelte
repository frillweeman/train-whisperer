<script lang="ts">
  import { streams, activeStream } from "../../stores/streams";

  $: inactiveStreams = $streams.filter(stream => stream !== $activeStream);
</script>

<div class="card shadow-xl">
  <header class="card-header h3 font-bold mb-6">
    <i class="fas fa-circle text-red-500 text-lg mr-2" />
    Inactive Streams
  </header>

  <!-- TODO: this can be componentized -->
  <section class="px-4">
    <ul class="divide-y divide-slate-500">
      {#each inactiveStreams as stream}
      <li class="py-4 flex justify-between items-center">
          <h3>{stream.title}</h3>
          <a href={`/live/${stream._id}`} class="btn btn-icon variant-soft hover:variant-soft-primary">
            <i class="fas fa-play text-lg" />
          </a>
        </li>
      {/each}
      {#if inactiveStreams.length === 0}
        <li class="py-4 flex justify-between items-center">
          <h3>No inactive streams</h3>
        </li>
      {/if}
    </ul>
  </section>
</div>
