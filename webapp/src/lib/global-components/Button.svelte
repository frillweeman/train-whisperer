<script>
  export let color = "primary";
  export let soft = false;
  export let variant = "filled";

  $: colorClass = `btn-${color}`;
  $: variantClass = `variant-${variant}`;
</script>

<button
  on:click
  class="btn {variantClass} {colorClass}"
>
  <slot />
</button>
