// Timing Defense v0.32 — waiting-room compact layout hotfix.
// Fixes FRIEND/LINK lower-content clipping on short Android landscape viewports.
(function(){
  const style=document.createElement('style');
  style.textContent=`
    #v027Waiting.v031Net .v027WaitBody{
      min-height:0!important;
      margin-top:6px!important;
    }
    #v027Waiting.v031Net .v027WaitPanel:first-child{
      box-sizing:border-box!important;
      display:flex!important;
      flex-direction:column!important;
      min-height:0!important;
      padding:10px 12px 9px!important;
      overflow:hidden!important;
    }
    #v027Waiting.v031Net .v027WaitTitle{
      flex:0 0 auto!important;
      font-size:16px!important;
      line-height:1.08!important;
    }
    #v027Waiting.v031Net .v027WaitSub{
      flex:0 0 auto!important;
      margin-top:4px!important;
      font-size:8px!important;
      line-height:1.35!important;
    }
    #v027Waiting.v031Net .v031Code{
      flex:0 0 auto!important;
      margin-top:5px!important;
      font-size:18px!important;
      line-height:1!important;
    }
    #v027Waiting.v031Net .v031State{
      flex:0 0 auto!important;
      margin-top:4px!important;
      font-size:7.2px!important;
      line-height:1.2!important;
    }
    #v027Waiting.v031Net .v031Status{
      flex:0 0 auto!important;
      margin-top:5px!important;
      padding:4px 7px!important;
      font-size:7.4px!important;
    }
    #v027Waiting.v031Net .v027LocalCard{
      flex:0 0 auto!important;
      margin-top:7px!important;
      padding:8px 9px!important;
    }
    #v027Waiting.v031Net .v027LocalTop{
      min-height:18px!important;
    }
    #v027Waiting.v031Net .v027Nick{
      font-size:11px!important;
    }
    #v027Waiting.v031Net .v027Class{
      font-size:8.5px!important;
    }
    #v027Waiting.v031Net .v027LocalCard .v027Truth{
      margin-top:5px!important;
      padding:6px 7px!important;
      font-size:7.2px!important;
      line-height:1.32!important;
    }
    #v027Waiting.v031Net .v027WaitActions{
      flex:0 0 auto!important;
      margin-top:6px!important;
      gap:6px!important;
      min-height:28px!important;
      align-items:center!important;
    }
    #v027Waiting.v031Net .v027WaitBtn{
      padding:6px 10px!important;
      font-size:8px!important;
      line-height:1!important;
    }
    #v027Waiting.v031Net .v031Msg{
      flex:0 0 auto!important;
      margin-top:4px!important;
      min-height:11px!important;
      font-size:7px!important;
      line-height:1.25!important;
    }
    #v027Waiting.v031Net .v031Copy{
      flex:0 0 auto!important;
      margin-top:4px!important;
      padding:5px 7px!important;
      min-height:0!important;
      max-height:24px!important;
      white-space:nowrap!important;
      overflow:hidden!important;
      text-overflow:ellipsis!important;
      word-break:normal!important;
      font-size:6.8px!important;
      line-height:1.2!important;
    }
    #v027Waiting.v031Net .v027WaitFoot{
      height:36px!important;
      min-height:36px!important;
      align-items:flex-end!important;
    }

    @media(max-height:590px){
      #v027Waiting.v031Net{
        padding:8px 14px 7px!important;
      }
      #v027Waiting.v031Net .v027WaitTop{
        min-height:28px!important;
      }
      #v027Waiting.v031Net .v027WaitBody{
        margin-top:4px!important;
        gap:8px!important;
      }
      #v027Waiting.v031Net .v027WaitPanel:first-child{
        padding:7px 9px 6px!important;
      }
      #v027Waiting.v031Net .v027WaitTitle{
        font-size:14px!important;
      }
      #v027Waiting.v031Net .v027WaitSub{
        margin-top:2px!important;
        font-size:7.2px!important;
      }
      #v027Waiting.v031Net .v031Code{
        margin-top:4px!important;
        font-size:16px!important;
      }
      #v027Waiting.v031Net .v031State{
        margin-top:3px!important;
        font-size:6.6px!important;
      }
      #v027Waiting.v031Net .v031Status{
        margin-top:4px!important;
        padding:3px 6px!important;
        font-size:6.8px!important;
      }
      #v027Waiting.v031Net .v027LocalCard{
        margin-top:5px!important;
        padding:6px 7px!important;
      }
      #v027Waiting.v031Net .v027Nick{
        font-size:10px!important;
      }
      #v027Waiting.v031Net .v027Class{
        font-size:7.7px!important;
      }
      #v027Waiting.v031Net .v027LocalCard .v027Truth{
        margin-top:3px!important;
        padding:4px 6px!important;
        font-size:6.6px!important;
        line-height:1.25!important;
      }
      #v027Waiting.v031Net .v027WaitActions{
        margin-top:4px!important;
        min-height:24px!important;
      }
      #v027Waiting.v031Net .v027WaitBtn{
        padding:5px 8px!important;
        font-size:7.3px!important;
      }
      #v027Waiting.v031Net .v031Msg{
        margin-top:3px!important;
        min-height:9px!important;
        font-size:6.4px!important;
      }
      #v027Waiting.v031Net .v031Copy{
        margin-top:3px!important;
        padding:4px 6px!important;
        max-height:20px!important;
        font-size:6.2px!important;
      }
      #v027Waiting.v031Net .v027WaitFoot{
        height:32px!important;
        min-height:32px!important;
      }
    }
  `;
  document.head.appendChild(style);
})();