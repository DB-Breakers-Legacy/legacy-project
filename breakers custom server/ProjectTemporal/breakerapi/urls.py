from django.urls import path
from . import views

urlpatterns = [

    #startup
    path("<pfx>/<id>/api/sys/get_env_v3", views.getEnv, name="getEnv"),
    path("<pfx>/<id>/api/user/auth", views.getUserAuth, name="getUserAuth"),
    path("<pfx>/<id>/api/user/get_country", views.getUserCountry, name="getUserCountry"),
    path("<pfx>/<id>/api/user/get_tracking_num", views.getTrackingNum, name="getTrackingNum"),

    #KPI - terms and agreement
    path("<pfx>/<id>/api/sys/agree_kpi", views.agreeKPI, name="agreeKPI"),
    path("dbtb-prd/<pfx>/<id>/api/sys/kpi", views.envKPI, name="envKPI"),

    #lobby
    path("dbtb-prd/<pfx>/<id>/api/close/get_close_info", views.getCloseInfo, name="getCloseInfo"),
    path("dbtb-prd/<pfx>/<id>/api/user/create_user_info", views.createUserInfo, name="createUserInfo"),
    path("dbtb-prd/<pfx>/<id>/api/adjustment_data_manage/read", views.readAdjustmentData, name="readAdjustmentData"),
    path("dbtb-prd/<pfx>/<id>/api/battle/get_stun_server_info", views.getStunServer, name="getStunServer"),
    path("dbtb-prd/<pfx>/<id>/api/patroller/get_status", views.getPatrollerStatus, name="getPatrollerStatus"),
    path("dbtb-prd/<pfx>/<id>/api/gamecurrency/get_owned", views.getGameCurrencyOwned, name="getGameCurrencyOwned"),
    
    #rivals/raider
    path("dbtb-prd/<pfx>/<id>/api/rival/get_list", views.getRivalList, name="getRivalList"),
    path("dbtb-prd/<pfx>/<id>/api/rival/skill_reset", views.rivalSkillReset, name="rivalSkillReset"),
    path("dbtb-prd/<pfx>/<id>/api/rival/training", views.rivalTraining, name="rivalTraining"),

    path("dbtb-prd/<pfx>/<id>/api/avatar_create/get_list", views.getAvatarCreateList, name="getAvatarCreateList"),
    path("dbtb-prd/<pfx>/<id>/api/character/get", views.getCharacter, name="getCharacter"),
    path("dbtb-prd/<pfx>/<id>/api/character/get_item", views.getCharacterItems, name="getCharacterItems"),
    path("dbtb-prd/<pfx>/<id>/api/battle/get_diarkis_matching_server_info", views.getMatchingServer, name="getMatchingServer"),
    path("dbtb-prd/<pfx>/<id>/api/user/get_ban_status", views.getBanStatus, name="getBanStatus"),
    path("dbtb-prd/<pfx>/<id>/api/commonpurchase/get_purchase_status", views.getPurchaseStatus, name="getPurchaseStatus"),
    path("dbtb-prd/<pfx>/<id>/api/item/item_possession", views.getItemPossession, name="getItemPossession"),
    path("dbtb-prd/<pfx>/<id>/api/battle/get_challenge_list", views.getChallengeList, name="getChallengeList"),
    path("dbtb-prd/<pfx>/<id>/api/event/get_schedule_list", views.getScheduleList, name="getScheduleList"),
    path("dbtb-prd/<pfx>/<id>/api/user/update_manner_point", views.updateMannerPoint, name="updateMannerPoint"),
    path("dbtb-prd/<pfx>/<id>/api/bnid_reward/grant_reward", views.grantReward, name="grantReward"),
    
    #messagebox
    path("dbtb-prd/<pfx>/<id>/api/message/get_message_list", views.getMessageList, name="getMessageList"),
    path("dbtb-prd/<pfx>/<id>/api/message/get_message_info", views.getMessageInfo, name="getMessageInfo"),
    path("dbtb-prd/<pfx>/<id>/api/message/update_message_item_received", views.updateMessageList, name="updateMessageList"),

    path("dbtb-prd/<pfx>/<id>/api/regularly_run/get_emergency_message", views.getEmergencyMessage, name="getEmergencyMessage"),
    path("dbtb-prd/<pfx>/<id>/api/news/get_3d_model_news", views.get3DModelNews, name="get3DModelNews"),
    path("dbtb-prd/<pfx>/<id>/api/lootbox/ticket_master_list", views.ticketMasterList, name="ticketMasterList"),
    path("dbtb-prd/<pfx>/<id>/api/leaderboard/get_leaderboard_model", views.getLeaderboardModel, name="getLeaderboardModel"),
    path("dbtb-prd/<pfx>/<id>/api/user/update_avatar", views.updateAvatar, name="updateAvatar"),
    
    #training
    path("dbtb-prd/<pfx>/<id>/api/transball/unlock_spattack", views.unlockSpattack, name="unlockSpattack"),
    path("dbtb-prd/<pfx>/<id>/api/skill/training", views.skillTraining, name="skillTraining"),
    
    #gacha
    
    #shop
    path("dbtb-prd/<pfx>/<id>/api/commonpurchase/tokusho/", views.tokusho, name="tokusho"),
]
