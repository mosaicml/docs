.. Mosaic documentation master file

Mosaic AI Training
================================

Databricks Mosaic AI Training enables Databricks customers to get started with custom code training with just a few simple steps. This offering is a separate SKU from other Generative AI offerings at Databricks, and requires access to the `Mosaic AI Training platform
<https://console.mosaicml.com/mosaicml/>`_, in addition to a Databricks workspace. 

Getting Started
---------------

Check out our `Getting Started <mcli/getting_started>`_ tutorial to start training AI models.

Reference Documentation
-----------------------

.. grid:: 2

    .. grid-item::
    
        .. card:: Mosaic AI CLI and SDK
            :link: mcli
            :class-footer: sd-font-italic

            Command Line Interface (CLI) and Python SDK

    .. grid-item::
    
        .. card:: Composer
            :link: https://docs.mosaicml.com/projects/composer
            :class-footer: sd-font-italic

            Open source training framework for large scale Generative AI models

    .. grid-item::
    
        .. card:: Streaming
            :link: https://docs.mosaicml.com/projects/streaming
            :class-footer: sd-font-italic

            Open source library for fast, accurate data streaming from cloud storage

    .. grid-item::
    
        .. card:: LLMFoundry
            :link: https://github.com/mosaicml/llm-foundry
            :class-footer: sd-font-italic

            Scripts for training, finetuning, and evaluating LLMs with Composer and MCLI

    .. grid-item::
    
        .. card:: Megablocks
            :link: https://github.com/databricks/megablocks
            :class-footer: sd-font-italic

            MegaBlocks is a light-weight library for mixture-of-experts (MoE) training. The core of the system is efficient "dropless-MoE" and standard MoE layers.

.. toctree::
   :caption: Mosaic AI
   :maxdepth: 2
   :hidden:

   mcli/index.rst
   composer/index.rst
   streaming/index.rst

   faq.md


.. _Twitter: https://twitter.com/DbrxMosaicAI
.. _Email: mailto:community@mosaicml.com
.. _Slack: https://mosaicml.me/slack
.. _Mosaic AI Blog: https://www.databricks.com/blog/category/generative-ai/mosaic-research