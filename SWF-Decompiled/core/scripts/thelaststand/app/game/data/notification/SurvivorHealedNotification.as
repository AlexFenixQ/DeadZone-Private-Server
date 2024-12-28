package thelaststand.app.game.data.notification
{
   import org.osflash.signals.Signal;
   import thelaststand.app.game.data.Survivor;
   import thelaststand.app.gui.dialogues.MessageBox;
   import thelaststand.app.network.Network;
   import thelaststand.common.gui.dialogues.Dialogue;
   import thelaststand.common.lang.Language;
   
   public class SurvivorHealedNotification implements INotification
   {
      private var _active:Boolean = false;
      
      private var _data:Survivor;
      
      private var _closed:Signal;
      
      public function SurvivorHealedNotification(param1:String)
      {
         super();
         this._closed = new Signal(INotification);
         this._data = Network.getInstance().playerData.compound.survivors.getSurvivorById(param1);
      }
      
      public function open() : void
      {
         var lang:Language;
         var dlg:MessageBox;
         var thisRef:INotification = null;
         if(this._data == null)
         {
            this._closed.dispatch(this);
            return;
         }
         thisRef = this;
         lang = Language.getInstance();
         dlg = new MessageBox(lang.getString("srv_healed_msg",this._data.fullName));
         dlg.addTitle(lang.getString("srv_healed_title",this._data.fullName),4671303);
         dlg.addButton(lang.getString("srv_healed_ok"));
         dlg.addImage(this._data.portraitURI,64,64);
         dlg.closed.addOnce(function(param1:Dialogue):void
         {
            _closed.dispatch(thisRef);
         });
         dlg.open();
      }
      
      public function get active() : Boolean
      {
         return this._active;
      }
      
      public function set active(param1:Boolean) : void
      {
         this._active = param1;
      }
      
      public function get closed() : Signal
      {
         return this._closed;
      }
      
      public function get type() : String
      {
         return NotificationType.SURVIVOR_HEALED;
      }
      
      public function get data() : *
      {
         return this._data;
      }
   }
}

